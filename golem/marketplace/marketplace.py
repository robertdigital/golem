from abc import ABC, abstractclassmethod, abstractmethod
from typing import Optional, List, TYPE_CHECKING

from dataclasses import dataclass

if TYPE_CHECKING:
    # pylint:disable=unused-import, ungrouped-imports
    from golem_messages.message.tasks import ReportComputedTask

class ProviderPerformance:
    def __init__(self, usage_benchmark: float):
        """
        Arguments:
            usage_benchmark {float} -- Use benchmark in seconds
        """
        self.usage_benchmark: float = usage_benchmark


@dataclass
class Offer:
    provider_id: str
    provider_performance: ProviderPerformance
    max_price: float
    price: float


@dataclass
class ProviderPricing:
    price_per_wallclock_h: int
    price_per_cpu_h: int


class RequestorMarketStrategy(ABC):

    @abstractclassmethod
    def add(cls, task_id: str, offer: Offer):
        """
        Called when a WantToComputeTask arrives.
        """
        raise NotImplementedError()

    # pylint: disable-msg=line-too-long
    @abstractclassmethod
    def resolve_task_offers(cls, task_id: str) -> Optional[List[Offer]]:
        """
        Arguments:
            task_id {str} -- task_id

        Returns:
            List[Offer] -- Returns a sorted list of Offers
        """
        raise NotImplementedError()

    @abstractclassmethod
    def get_task_offer_count(cls, task_id: str) -> int:
        """
        Returns number of offers known for the task.
        """
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def calculate_payment(cls, rct: 'ReportComputedTask') -> int:
        raise NotImplementedError()


class ProviderMarketStrategy(ABC):

    @abstractclassmethod
    def calculate_price(cls, pricing: ProviderPricing, max_price: int,
                        requestor_id: str) -> int:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def calculate_payment(cls, rct: 'ReportComputedTask') -> int:
        raise NotImplementedError()
