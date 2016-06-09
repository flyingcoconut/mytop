class Collector(object):
    def __init__(self):
        self.metrics = {}

    def add_metric(self, metric):
        """Add a new metric"""
        self.metrics[metric.name] = metric

    def remove_metric(self, name):
        """Remove a metric with name"""
        del(self.metrics[name])

    def list_metrics(self):
        """List all possible metrics"""
        metrics = []
        for m in self._metrics:
            metrics.append(m)
        return metrics

    def enable_metric(self, name):
        """Enable a metric"""
        self.metrics[name].enable()

    def disable_metric(self, name):
        """Disable a specific metric"""
        self.metrics[name].disable()


