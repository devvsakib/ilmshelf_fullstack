from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.core.auth import get_current_user

from app.services import statistics_service

from app.schemas.statistics_schema import (
    StatisticsResponse,
    MonthlyStatisticsResponse,
    YearlyStatisticsResponse,
)

router = APIRouter()


@router.get(
    "/",
    response_model=StatisticsResponse,
)
def get_statistics(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return statistics_service.get_statistics(
        current_user.id,
        db,
    )


@router.get(
    "/monthly",
    response_model=list[MonthlyStatisticsResponse],
)
def monthly_statistics(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return statistics_service.get_monthly_statistics(
        current_user.id,
        db,
    )


@router.get(
    "/yearly",
    response_model=list[YearlyStatisticsResponse],
)
def yearly_statistics(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return statistics_service.get_yearly_statistics(
        current_user.id,
        db,
    )
