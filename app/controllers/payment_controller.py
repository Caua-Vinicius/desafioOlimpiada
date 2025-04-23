from fastapi import APIRouter

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.get("/calculate/{value}/{amount}")
def calculate(value: float, amount: int):
    installments = []
    base_value = value / amount
    rounded_value = round(base_value, 2)

    total = 0.0
    for i in range(1, amount + 1):
        if i == amount:
            last_value = round(value - total, 2)
            installments.append({"order": i, "value": last_value})
        else:
            installments.append({"order": i, "value": rounded_value})
            total += rounded_value

    return {
        "value": value,
        "amount": amount,
        "installments": installments
    }