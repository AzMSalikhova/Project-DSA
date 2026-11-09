from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from app.auth import get_current_user
from app.templates import templates
from app.database import SessionLocal
from app.models.flights import Flight
from app.structures import MyHashMap, SegmentTree, BinarySearch, BinaryHeap, calculate_pagerank

router = APIRouter()

hash_map = MyHashMap()
all_delays = []
st = None
bs = None
top_airports = []
flight_queue = BinaryHeap()

def load_structures():
    global st, bs
    if len(all_delays) > 0:
        return

    print("Сейчас идет загрузка таблицы из файла...")
    db = SessionLocal()
    try:
        flights = db.query(Flight).all()
        routes = []
        print(f"Строится HashMap...")

        for f in flights:
            flight_dict = {
                "flight_id": f.flight_id,
                "airline": f.airline,
                "origin_airport": f.origin_airport,
                "destination_airport": f.destination_airport,
                "departure_delay_min": f.departure_delay_min,
                "aircraft_type": f.aircraft_type,
                "weather_condition": f.weather_condition,
                "passenger_count": f.passenger_count,
                "ticket_revenue_usd": f.ticket_revenue_usd
            }
            hash_map.put(f.flight_id, flight_dict)
            all_delays.append(f.departure_delay_min)

            routes.append((f.origin_airport, f.destination_airport))

            if f.departure_delay_min > 100 and len(flight_queue.heap) < 10:
                flight_queue.insert(f.flight_id, f.departure_delay_min)

        print("Строится SegmentTree...")
        st = SegmentTree(all_delays)
        bs = BinarySearch(all_delays)

        print("Ранжирование...")
        global top_airports
        top_airports = calculate_pagerank(routes, num_iterations=10)

        print("Алгоритмы успешно загружены!")
    except Exception as e:
        print(f"Не получилось загрузить данные: {e}")
    finally:
        db.close()


def require_user(request: Request):
    user = get_current_user(request)
    if user is None:
        return RedirectResponse(
            "/login",
            status_code=302
        )
    return user


@router.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse("/dashboard")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, error: str = None):
    user = require_user(request)
    if isinstance(user, RedirectResponse):
        return user

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "flight": None,
            "error": error
        })


@router.post("/api/search", response_class=HTMLResponse)
def search_flight(request: Request, flight_id: str = Form()):
    if isinstance(require_user(request), RedirectResponse):
        return require_user(request)

    found_flight = hash_map.get(flight_id)
    if found_flight:
        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={"flight": found_flight}
        )
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"error": f"Рейс {flight_id} не найден"}
    )


@router.get("/analytics", response_class=HTMLResponse)
def analytics(
        request: Request,
        sum_result: int = None,
        l: int = None,
        r: int = None,
        threshold_result: int = None,
        k: int = None,
        error: str = None
    ):
    if isinstance(require_user(request), RedirectResponse):
        return require_user(request)
    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={
            "sum_result": sum_result, "l": l, "r": r,
            "threshold_result": threshold_result, "k": k, "error": error,
            "top_airports": top_airports,
            "flight_queue": flight_queue
        })


@router.post("/api/range_sum", response_class=HTMLResponse)
def get_range_sum(request: Request, l: int = Form(), r: int = Form()):
    if isinstance(require_user(request), RedirectResponse):
        return require_user(request)

    try:
        total = st.query(l, r)
        return templates.TemplateResponse(
            request=request,
            name="analytics.html",
            context={
                "sum_result": total,
                "l": l,
                "r": r,
                "top_airports": top_airports,
                "flight_queue": flight_queue
            })

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="analytics.html",
            context={"error": str(e),
                     "top_airports": top_airports,
                     "flight_queue": flight_queue
            })


@router.post("/api/binary_search", response_class=HTMLResponse)
def get_threshold(request: Request, k: int = Form()):
    if isinstance(require_user(request), RedirectResponse):
        return require_user(request)
    threshold = bs.find_threshold(k)

    if threshold is not None:
        return templates.TemplateResponse(
            request=request,
            name="analytics.html",
            context={
                "threshold_result": threshold,
                "k": k,
                "top_airports": top_airports,
                "flight_queue": flight_queue
            })

    return templates.TemplateResponse(
        request=request,
        name="analytics.html",
        context={"error": "Недостаточно рейсов",
                 "top_airports": top_airports,
                 "flight_queue": flight_queue
                 })