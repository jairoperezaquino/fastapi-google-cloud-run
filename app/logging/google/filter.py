import logging
import re

from google.cloud.logging_v2.handlers import CloudLoggingFilter

from app.logging.google.middleware import http_request_context, cloud_trace_context


class GoogleCloudLogFilter(CloudLoggingFilter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.http_request = http_request_context.get()

        trace = cloud_trace_context.get()
        if not trace:  # If no trace, avoid unnecessary processing
            return super().filter(record)

        split_header = trace.split("/", 1)
        record.trace = f"projects/{self.project}/traces/{split_header[0]}"

        if len(split_header) > 1:
            header_suffix = split_header[1]
            span_id_match = re.findall(r"^\w+", header_suffix)
            if span_id_match:
                record.span_id = span_id_match[0]

        return super().filter(record)
