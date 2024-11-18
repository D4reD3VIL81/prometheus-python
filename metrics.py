from prometheus_client import start_http_server, Counter, Gauge, Histogram, Summary
from typing import Optional, Union, Dict


class Metrics:
    """
    Abstraction class for managing Prometheus metrics.
    Provides methods to define and manipulate Prometheus metrics such as counters, gauges, histograms, and summaries.
    """

    def __init__(self, port: int):
        """
        Initialize the Metrics class with the HTTP server port.
        Args:
            port (int): Port to start the Prometheus HTTP server.
        """
        if not isinstance(port, int) or port <= 0:
            raise ValueError("Port must be a positive integer.")

        self.port = port
        self.metrics = {
            "counter": {},
            "gauge": {},
            "histogram": {},
            "summary": {}
        }

    def initiate_http_server(self) -> None:
        """
        Start the Prometheus HTTP server on the specified port.
        Raises:
            RuntimeError: If the server fails to start.
        """
        try:
            start_http_server(port=self.port)
        except Exception as e:
            raise RuntimeError(f"Failed to start HTTP server on port {self.port}: {e}")

    def define_counter(self, name: str, description: str, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Define a Prometheus counter metric.
        Args:
            name (str): Name of the counter.
            description (str): Description of the counter.
            labels (Optional[Dict[str, str]]): Dictionary of label names and default values.
        Raises:
            ValueError: If the name already exists.
        """
        if name in self.metrics["counter"]:
            raise ValueError(f"Counter with name '{name}' already exists.")

        self.metrics["counter"][name] = Counter(name, description, labelnames=labels.keys() if labels else None)

    def define_gauge(self, name: str, description: str, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Define a Prometheus gauge metric.
        Args:
            name (str): Name of the gauge.
            description (str): Description of the gauge.
            labels (Optional[Dict[str, str]]): Dictionary of label names and default values.
        Raises:
            ValueError: If the name already exists.
        """
        if name in self.metrics["gauge"]:
            raise ValueError(f"Gauge with name '{name}' already exists.")

        self.metrics["gauge"][name] = Gauge(name, description, labelnames=labels.keys() if labels else None)

    def define_histogram(self, name: str, description: str, buckets: Optional[list] = None,
                         labels: Optional[Dict[str, str]] = None) -> None:
        """
        Define a Prometheus histogram metric.
        Args:
            name (str): Name of the histogram.
            description (str): Description of the histogram.
            buckets (Optional[list]): List of bucket boundaries for the histogram.
            labels (Optional[Dict[str, str]]): Dictionary of label names and default values.
        Raises:
            ValueError: If the name already exists or buckets are invalid.
        """
        if name in self.metrics["histogram"]:
            raise ValueError(f"Histogram with name '{name}' already exists.")

        if buckets and not all(isinstance(b, (int, float)) for b in buckets):
            raise ValueError("Buckets must be a list of numbers.")

        self.metrics["histogram"][name] = Histogram(name, description, buckets=buckets,
                                                    labelnames=labels.keys() if labels else None)

    def define_summary(self, name: str, description: str, objectives: Optional[dict] = None,
                       labels: Optional[Dict[str, str]] = None) -> None:
        """
        Define a Prometheus summary metric.
        Args:
            name (str): Name of the summary.
            description (str): Description of the summary.
            objectives (Optional[dict]): Map of quantile to error.
            labels (Optional[Dict[str, str]]): Dictionary of label names and default values.
        Raises:
            ValueError: If the name already exists or objectives are invalid.
        """
        if name in self.metrics["summary"]:
            raise ValueError(f"Summary with name '{name}' already exists.")

        if objectives and not all(
                isinstance(k, (int, float)) and isinstance(v, (int, float)) for k, v in objectives.items()):
            raise ValueError("Objectives must be a dictionary of numbers.")

        self.metrics["summary"][name] = Summary(name, description, objectives=objectives,
                                                labelnames=labels.keys() if labels else None)

    def increment_counter(self, name: str, amount: int = 1, labels: Optional[Dict[str, str]] = None) -> None:
        """
        Increment a counter metric.
        Args:
            name (str): Name of the counter.
            amount (int): Amount to increment (default is 1).
            labels (Optional[Dict[str, str]]): Dictionary of label values to associate with this increment.
        Raises:
            KeyError: If the counter does not exist.
        """
        if name not in self.metrics["counter"]:
            raise KeyError(f"Counter with name '{name}' does not exist.")

        metric = self.metrics["counter"][name]
        if labels:
            metric.labels(**labels).inc(amount)
        else:
            metric.inc(amount)

    def increment_gauge(self, name: str, amount: Union[int, float] = 1,
                        labels: Optional[Dict[str, str]] = None) -> None:
        """
        Increment a gauge metric.
        Args:
            name (str): Name of the gauge.
            amount (Union[int, float]): Amount to increment (default is 1).
            labels (Optional[Dict[str, str]]): Dictionary of label values to associate with this increment.
        Raises:
            KeyError: If the gauge does not exist.
        """
        if name not in self.metrics["gauge"]:
            raise KeyError(f"Gauge with name '{name}' does not exist.")

        metric = self.metrics["gauge"][name]
        if labels:
            metric.labels(**labels).inc(amount)
        else:
            metric.inc(amount)

    def decrement_gauge(self, name: str, amount: Union[int, float] = 1,
                        labels: Optional[Dict[str, str]] = None) -> None:
        """
        Decrement a gauge metric.
        Args:
            name (str): Name of the gauge.
            amount (Union[int, float]): Amount to decrement (default is 1).
            labels (Optional[Dict[str, str]]): Dictionary of label values to associate with this decrement.
        Raises:
            KeyError: If the gauge does not exist.
        """
        if name not in self.metrics["gauge"]:
            raise KeyError(f"Gauge with name '{name}' does not exist.")

        metric = self.metrics["gauge"][name]
        if labels:
            metric.labels(**labels).dec(amount)
        else:
            metric.dec(amount)

    def record_histogram(self, name: str, value: Union[int, float], labels: Optional[Dict[str, str]] = None) -> None:
        """
        Record a value in a histogram metric.
        Args:
            name (str): Name of the histogram.
            value (Union[int, float]): Value to record.
            labels (Optional[Dict[str, str]]): Dictionary of label values to associate with this observation.
        Raises:
            KeyError: If the histogram does not exist.
        """
        if name not in self.metrics["histogram"]:
            raise KeyError(f"Histogram with name '{name}' does not exist.")

        metric = self.metrics["histogram"][name]
        if labels:
            metric.labels(**labels).observe(value)
        else:
            metric.observe(value)

    def record_summary(self, name: str, value: Union[int, float], labels: Optional[Dict[str, str]] = None) -> None:
        """
        Record a value in a summary metric.
        Args:
            name (str): Name of the summary.
            value (Union[int, float]): Value to record.
            labels (Optional[Dict[str, str]]): Dictionary of label values to associate with this observation.
        Raises:
            KeyError: If the summary does not exist.
        """
        if name not in self.metrics["summary"]:
            raise KeyError(f"Summary with name '{name}' does not exist.")

        metric = self.metrics["summary"][name]
        if labels:
            metric.labels(**labels).observe(value)
        else:
            metric.observe(value)