import logging
import re
import csv
import homework.log_const

def check_date(data_type, data):
    # first name
    if data_type == 'fname':
        if data is int:
            raise TypeError('Incorrect first name type')
        if (re.search(r'\d', data)) is None:
            if re.match(r'\w+\b', data):
                return data
            else:
                raise ValueError('Incorrect first name value')
        else:
            raise ValueError('Incorrect first name value')
    # second name
    if data_type == 'sname':
        if data is int:
            raise TypeError('Incorrect second name type')
        if (re.search(r'\d', data)) is None:
            if re.match(r'\w+\b', data):
                return data
            else:
                raise ValueError('Incorrect second name value')
        else:
            raise ValueError('Incorrect second name value')
    # birth date
    if data_type == 'bdate':
        data = re.split('-', data)
        data = ''.join(data)
        if re.search(r'\D', data) is None:
            data = re.findall(r'\d+', data)
            data = ''.join(data)
            if len(data) == 8:
                return data[0:4] + '-' + data[4:6] + '-' + data[6:]
            else:
                raise ValueError('Incorrect birth date value')
        else:
            raise ValueError('Incorrect birth date value')
    # phone
    if data_type == 'phone':
        if re.search(r'[^\d()\-+ ]', data) is None:
            data = re.findall(r'\d+', data)
            data = ''.join(data)
            if len(data) == 11:
                return '8' + data[1:]
            else:
                raise ValueError('Incorrect phone value')
        else:
            raise ValueError('Incorrect phone value')

    # document type
    if data_type == 'dtype':
        if data is int:
            raise TypeError('Incorrect document name type')
        types = ('Паспорт', 'паспорт', 'Заграничный паспорт',
                 'заграничный паспорт', 'загран',
                 'Водительские права', 'водительсикие права')
        if (re.search(r'\d', data)) is None:
            if data in types:
                return data
            else:
                raise ValueError('Incorrect doc id value')
        else:
            raise ValueError('Incorrect doc id value')
    # document number
    if data_type == 'docid':
        if re.search(r'[^\d ]]', data) is None:
            data = re.findall(r'\d+', data)
            data = ''.join(data)
            if len(data) == 10 or len(data) == 9:
                return data
            else:
                raise ValueError('Incorrect doc num value')
        else:
            raise ValueError('Incorrect doc num value')


def Logger(func):
    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, *kwargs)
        except TypeError:
            self.ex_log.error('Incorrect input type')
            raise TypeError('Incorrect Type')
        except ValueError:
            self.ex_log.error('Incorrect input value')
            raise ValueError('Incorrect value')
        else:
            self.log.info('{0} {1}: {2} was successfully set to {3}'.format(self.first_name,
                                                                            self.last_name, func.__name__, args[0]))
    return wrapper


class Patient(object):
    def __init__(self, first_name, second_name, birth_date, phone, document_type, document_id):
        self.ex_log = logging.getLogger('Exception_Logger')
        self.log = logging.getLogger('Logger')

        try:
            self.__first_name = check_date('fname', first_name)
            self.__last_name = check_date('sname', second_name)
            self.birth_date_ = check_date('bdate', birth_date)
            self.phone_ = check_date('phone', phone)
            self.document_type_ = check_date('dtype', document_type)
            self.document_id_ = check_date('docid', document_id)
        except TypeError as error_text:
            self.ex_log.error('Incorrect input value')
            raise TypeError(error_text)
        except ValueError as error_text:
            self.ex_log.error('Incorrect input value')
            raise ValueError(error_text)
        else:
            self.log.info('New patient.py added: %s %s, %s, %s, %s %s' %
                          (first_name, second_name, birth_date, phone, document_type, document_id))

    @classmethod
    def create(cls, *args):
        return cls(*args)

    def save(self, path='PatientsCollection.csv'):
        try:
            with open(path, 'a', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                patient = [self.__first_name, self.__last_name, self.birth_date_,
                           self.phone_, self.document_type_, self.document_id_]
                writer.writerow(patient)
        except Exception:
            self.ex_log.error('Saving was unsuccessful')
            raise Exception('Saving was unsuccessful')
        else:
            self.log.info('Patient %s %s was successfuly added to file' % (self.__first_name, self.__last_name))

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        self.ex_log.error('Unable to rewrite FIRST_NAME')
        raise AttributeError("You can't change this field")

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.ex_log.error('Unable to rewrite SECOND_NAME')
        raise AttributeError("You can't change this field")

    @property
    def birth_date(self):
        return self.birth_date_

    @birth_date.setter
    @Logger
    def birth_date(self, value):
        self.birth_date_ = check_date('bdate', value)

    @property
    def phone(self):
        return self.phone_

    @phone.setter
    @Logger
    def phone(self, value):
        self.phone_ = check_date('phone', value)

    @property
    def document_type(self):
        return self.document_type_

    @document_type.setter
    @Logger
    def document_type(self, value):
        self.document_type_ = check_date('dtype', value)

    @property
    def document_id(self):
        return self.document_id_

    @document_id.setter
    @Logger
    def document_id(self, value):
        self.document_id_ = check_date('docid', value)

    def __del__(self):
        del self.log, self.ex_log
        for fh in list(logging.getLogger('Exception_Logger').handlers)[::-1]:
            fh.close()
        for fh in list(logging.getLogger('Logger').handlers)[::-1]:
            fh.close()


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
        del self.log, self.ex_log
        for fh in list(logging.getLogger('Exception_Logger').handlers)[::-1]:
            fh.close()
        for fh in list(logging.getLogger('Logger').handlers)[::-1]:
            fh.close()
