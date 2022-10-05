import usys
import utime


_loggers = {}


def set_logger(name, dest, *args, **kwargs):
    _loggers[name] = _logger(name, dest, *args, **kwargs)
    return _loggers[name]


def file_log(filename):
    return _destination_point(_destination_point.FILE, filename=filename)


def stdout_log():
    return _destination_point(_destination_point.STDOUT)


class _destination_point:
    FILE = 0
    STDOUT = 1
    
    def __init__(self, type_, **artifacts):
        if type_ == self.FILE:
            self.filename = artifacts['filename']
            self.write = self._write_to_file
        elif type_ == self.STDOUT:
            self.write = self._write_to_stdout
        
    def _write_to_file(self, msg):
        with open(self.filename, 'a') as fh:
            fh.write(msg)
            fh.write('\n')

    def _write_to_stdout(self, msg):
        usys.stdout.write(msg)
        usys.stdout.write('\n')


class ParserError(Exception):
    pass


class _logger:    
    TIME_FIELD_NAME = 'time'
    LOGGER_FIELD_NAME = 'logger'
    LEVEL_FIELD_NAME = 'level'
    MESSAGE_FIELD_NAME = 'message'

    DEBUG_LEVEL_LABEL = 'DEBUG'
    INFO_LEVEL_LABEL = 'INFO'
    WARNING_LEVEL_LABEL = 'WARNING'
    ERROR_LEVEL_LABEL = 'ERROR'
    CRITICAL_LEVEL_LABEL = 'CRITICAL'

    DEBUG_LEVEL_NUMERIC_VALUE = 10
    INFO_LEVEL_NUMERIC_VALUE = 20
    WARNING_LEVEL_NUMERIC_VALUE = 30
    ERROR_LEVEL_NUMERIC_VALUE = 40
    CRITICAL_LEVEL_NUMERIC_VALUE = 50

    def __init__(self, name, dest, loglevel=WARNING_LEVEL_NUMERIC_VALUE, format='|<time>|<logger>|<level>|<message>'):
        self.name = name
        self.dest = dest
        self.loglevel = loglevel
        self.format = self._insert_value_in_log_line(format, self.LOGGER_FIELD_NAME, name)
    
    def debug(self, msg):
        if 0 >= self.loglevel:
            self.log(msg, self.DEBUG_LEVEL_LABEL)
        
    def info(self, msg):
        if 1 >= self.loglevel:
            self.log(msg, self.INFO_LEVEL_LABEL)
        
    def warning(self, msg):
        if 2 >= self.loglevel:
            self.log(msg, self.WARNING_LEVEL_LABEL)
    
    def error(self, msg):
        if 3 >= self.loglevel:
            self.log(msg, self.ERROR_LEVEL_LABEL)

    def critical(self, msg):
        if 3 >= self.loglevel:
            self.log(msg, self.CRITICAL_LEVEL_LABEL)
        
    def log(self, msg, level):
        log_line = self._insert_value_in_log_line(self.format, self.TIME_FIELD_NAME, self._datetime()) 
        log_line = self._insert_value_in_log_line(log_line, self.LEVEL_FIELD_NAME, level)
        log_line = self._insert_value_in_log_line(log_line, self.MESSAGE_FIELD_NAME, msg)
        self.dest.write(log_line)
        
    def _insert_value_in_log_line(self, line, field, value):
        field_prefix = '<' + field
        if field_prefix in line:
            line_chunks = line.split(field_prefix, 1)
            if line_chunks[1] and line_chunks[1][0] == ':' and '>' in line_chunks[1][1:]:
                field_suffix_chunks = line_chunks[1].lstrip(':').split('>', 1)
                padding = self._prepare_padding(
                    value=field_suffix_chunks[0], 
                    error_message="Padding for field should be integer: {}".format(field_suffix_chunks[0])
                )
                line = line_chunks[0] + padding.format(value) + field_suffix_chunks[1]
                return self._insert_value_in_log_line(line, field, value)
            elif line_chunks[1] and line_chunks[1][0] == '>':
                line = line_chunks[0] + str(value) + line_chunks[1].lstrip('>')
                return self._insert_value_in_log_line(line, field, value)
        return line

    def _prepare_padding(self, value, error_message="Padding for field should be integer"):
        try:
            padding = '{0: <' + str(int(value)) + '}'
        except ValueError:
            raise ParserError(error_message)
        return padding
    
    def _datetime(self, format='{year}-{months}-{days} {hours}:{minutes}:{seconds}'):
        required_fields = ['{year}', '{months}', '{days}', '{hours}', '{minutes}', '{seconds}']
        for field in required_fields:
            if field not in format:
                raise ValueError("Datetime's format should contain all fileds: " + ", ".join(required_fields))
        local_time = utime.localtime()
        year = str(local_time[0])
        months = str(local_time[1]) if local_time[1] > 9 else '0' + str(local_time[1])
        days = str(local_time[2]) if local_time[2] > 9 else '0' + str(local_time[2])
        hours = str(local_time[3]) if local_time[3] > 9 else '0' + str(local_time[3])
        minutes = str(local_time[4]) if local_time[4] > 9 else '0' + str(local_time[4])
        seconds = str(local_time[5]) if local_time[5] > 9 else '0' + str(local_time[5])
        return format.format(year=year, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds)
