import logging
import re
import csv
import homework.log_const


def check_name(data):
    if not isinstance(data, str):
        raise TypeError("Incorrect name type: " + str(data))
    if re.match(r'\w+\b', data) and not re.search(r'\d', data):
        return data
    else:
        raise ValueError('Incorrect name value: ' + str(data))


def logging_decorator(func):
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
        except TypeError as er_text:
            # er_text = 'Patient{0} {1}: incorrect type for function {2}'\
            #    .format(self.first_name, self.last_name, func.__name__)
            logging.getLogger('Exception_Logger').error(er_text)
            raise TypeError(er_text)
        except ValueError as er_text:
            logging.getLogger('Exception_Logger').error(er_text)
            raise ValueError(er_text)
        except IsADirectoryError as er_text:
            logging.getLogger('Exception_Logger').error(er_text)
            raise IsADirectoryError(er_text)
        except PermissionError as er_text:
            logging.getLogger('Exception_Logger').error(er_text)
            raise PermissionError(er_text)
        except AttributeError as er_text:
            logging.getLogger('Exception_Logger').error(er_text)
            raise AttributeError(er_text)
        finally:
            pass
        logging.getLogger('Logger').info('Function {0} was successfully done for patient {1} {2}'
                                         .format(func.__name__, self.first_name, self.last_name))
        return result
    return wrapper


class Patient(object):
    @logging_decorator
    def __init__(self, first_name, second_name, birth_date, phone, document_type, document_id):
        try:
            logging.getLogger('Logger').disabled = True  # костыыыыыль
            self.first_name_ = check_name(first_name)
            self.last_name_ = check_name(second_name)
            self.birth_date = birth_date
            self.phone = phone
            self.document_type = document_type
            self.document_id = document_id
            logging.getLogger('Logger').disabled = False
        except TypeError as error_text:
            raise TypeError(error_text)
        except ValueError as error_text:
            raise ValueError(error_text)

    @staticmethod
    def create(*args):
        return Patient(*args)

    @logging_decorator
    def save(self, path='PatientsCollection.csv'):
        try:
            with open(path, 'a', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                patient = [self.first_name, self.last_name, self.birth_date_,
                           self.phone_, self.document_type_, self.document_id_]
                writer.writerow(patient)
        except IsADirectoryError:
            raise IsADirectoryError('%s %s:Saving was unsuccessful: incorrect path' % (self.first_name, self.last_name))
        except PermissionError:
            raise PermissionError('%s %s:Saving was unsuccessful: PermissionError' % (self.first_name, self.last_name))

    @property
    def first_name(self):
        return self.first_name_

    @first_name.setter
    @logging_decorator
    def first_name(self, value):
        raise AttributeError("%s %s: You can't change this field" % (self.first_name, self.last_name))

    @property
    def last_name(self):
        return self.last_name_

    @last_name.setter
    @logging_decorator
    def last_name(self, value):
        raise AttributeError("%s %s: You can't change this field" % (self.first_name, self.last_name))

    @property
    def birth_date(self):
        return self.birth_date_

    @birth_date.setter
    @logging_decorator
    def birth_date(self, value):
        if not isinstance(value, str):
            raise TypeError("%s %s: unable to change birth date because of incorrect TYPE"
                            % (self.first_name, self.last_name))
        if re.match(r'\d{4}-\d{2}-\d{2}\b', value):
            self.birth_date_ = value
        else:
            raise ValueError("%s %s: unable to change birth date because of incorrect VALUE"
                             % (self.first_name, self.last_name))

    @property
    def phone(self):
        return self.phone_

    @phone.setter
    @logging_decorator
    def phone(self, value):
        if not isinstance(value, str):
            raise TypeError("%s %s: unable to change phone because of incorrect TYPE"
                            % (self.first_name, self.last_name))
        if re.search(r'[^\d()\-+ ]', value) is None:
            data = re.findall(r'\d+', value)
            data = ''.join(data)
            if len(data) == 11:
                self.phone_ = '8' + data[1:]
            else:
                raise ValueError("%s %s: unable to change phone because of incorrect VALUE"
                                 % (self.first_name, self.last_name))
        else:
            raise ValueError("%s %s: unable to change phone because of incorrect VALUE"
                             % (self.first_name, self.last_name))

    @property
    def document_type(self):
        return self.document_type_

    @document_type.setter
    @logging_decorator
    def document_type(self, value):
        if not isinstance(value, str):
            raise TypeError("%s %s: unable to change doc. type because of incorrect TYPE"
                            % (self.first_name, self.last_name))
        types = ('паспорт', 'заграничный паспорт', 'водительские права')
        if value in types:
            self.document_type_ = value
        else:
            raise ValueError("%s %s: unable to change doc. type because of incorrect VALUE"
                             % (self.first_name, self.last_name))

    @property
    def document_id(self):
        return self.document_id_

    @document_id.setter
    @logging_decorator
    def document_id(self, value):
        if not isinstance(value, str):
            raise TypeError("%s %s: unable to change doc. id because of incorrect TYPE"
                            % (self.first_name, self.last_name))
        if re.search(r'[^\d ]]', value) is None:
            value = re.findall(r'\d+', value)
            value = ''.join(value)
            if (len(value) == 10 and self.document_type_ != 'заграничный паспорт') or\
                    (len(value) == 9 and self.document_type_ == 'заграничный паспорт'):
                self.document_id_ = value
            else:
                raise ValueError("%s %s: unable to change doc. id because of incorrect VALUE"
                                 % (self.first_name, self.last_name))
        else:
            raise ValueError("%s %s: unable to change doc. id because of incorrect VALUE"
                             % (self.first_name, self.last_name))

    def __del__(self):
        homework.log_const.fh1.close()
        homework.log_const.fh2.close()


class PatientCollection:
    def __init__(self, path_to_file):
        self.ex_log = logging.getLogger('Exception_Logger')
        self.log = logging.getLogger('Logger')

        self.path_to_file = path_to_file

    def limit(self, value):
        with open(self.path_to_file, 'rb', buffering=0) as file:
            line = file.readline()
            i = 0
            while i < value and line:
                line = re.split(',', line.decode('utf-8'))
                yield Patient(*line)
                line = file.readline()
                i += 1

    def __iter__(self):
        with open(self.path_to_file, 'rb', buffering=0) as file:
            line = file.readline()
            while line:
                line = re.split(',', line.decode('utf-8'))
                yield Patient(*line)
                line = file.readline()

    def __del__(self):
        homework.log_const.fh1.close()
        homework.log_const.fh2.close()


