from logging import LoggerAdapter


class ExtendableLogsAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        if not self.extra:
            return msg, kwargs
        
        extra_fields = []

        for key in self.extra:
            extra_fields.append(f"[{key}: {self.extra.get(key)}]")

        extra_string = "".join(extra_fields)
        return f'{extra_string} - {msg}', kwargs
