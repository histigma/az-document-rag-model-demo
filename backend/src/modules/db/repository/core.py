from typing import TYPE_CHECKING, Iterable, TypeVar, Generic
from dataclasses import dataclass

if TYPE_CHECKING:
    from weaviate.collections.classes.internal import Object

TQueryObjects = TypeVar("TQueryObjects", bound=object)

@dataclass
class RepoQueryResult(Generic[TQueryObjects]):
    query: list[TQueryObjects]


class WeaviateRepoQueryResult(RepoQueryResult["Object"]):
    def filter_gen(
        self,
        distance_limit: float = 0.5,
        limit: int | None = None,
    ) -> Iterable["Object"]:
        """
        Lazy evaluation filter for Weaviate query results.
        Only yields objects with distance <= distance_limit.
        """
        count = 0
        for obj in self.query:
            distance = getattr(obj.metadata, "distance", None)
            if distance is None:
                continue

            if distance <= distance_limit:
                yield obj
                count += 1
                if limit is not None and count >= limit:
                    break

