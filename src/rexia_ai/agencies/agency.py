"""Agency class for ReXia AI."""

from ..tasks import AgencyTask
from ..agents import ManagerAgent
from ..common import AgencyStatus


class Agency:
    """Agency Class."""

    def __init__(
        self,
        manager: ManagerAgent,
        tasks: list[AgencyTask],
        verbose: bool = True,
    ):
        """Initialize the agency."""
        self.manager = manager
        self.tasks = tasks
        self.verbose = verbose
        self.status = AgencyStatus.IDLE

    def launch(self):
        """Launch the agency."""
        self.status = AgencyStatus.WORKING
        if self.verbose:
            print(f"Agency {self.__class__.__name__} is now working.")
        
        # Run the manager agent
        return self.manager.plan(self.tasks)
