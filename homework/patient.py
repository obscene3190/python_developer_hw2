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


def raise_error(ex_log, er_type, data, value):
    text = "{0} didn't changed to {1} because of incorrect {2}".format(data, value, er_type)
    if er_type == 'value':
        ex_log.error(text)
        raise ValueError(text)
    elif er_type == 'type':
        ex_log.error(text)
        raise TypeError(text)


class Patient(object):
    def __init__(self, first_name, second_name, birth_date, phone, document_type, document_id):
        self.ex_log = logging.getLogger('Exception_Logger')
        self.log = logging.getLogger('Logger')
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
            self.ex_log.error(error_text)
            raise TypeError(error_text)
        except ValueError as error_text:
            self.ex_log.error(error_text)
            raise ValueError(error_text)
        else:
            self.log.info('New patient.py added: %s %s, %s, %s, %s %s' %
                          (first_name, second_name, birth_date, phone, document_type, document_id))

    @staticmethod
    def create(*args):
        return Patient(*args)

    def save(self, path='PatientsCollection.csv'):
        try:
            with open(path, 'a', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                patient = [self.__first_name, self.__last_name, self.birth_date_,
                           self.phone_, self.document_type_, self.document_id_]
                writer.writerow(patient)
        except IsADirectoryError:
            self.ex_log.error('%s %s:Saving was unsuccessful: incorrect path' % (self.first_name, self.last_name))
            raise IsADirectoryError('%s %s:Saving was unsuccessful: incorrect path' % (self.first_name, self.last_name))
        except PermissionError:
            self.ex_log.error('%s %s:Saving was unsuccessful: PermissionError ' % (self.first_name, self.last_name))
            raise PermissionError('%s %s:Saving was unsuccessful: PermissionError' % (self.first_name, self.last_name))
        else:
            self.log.info('Patient %s %s was successfully added to file' % (self.__first_name, self.__last_name))

    @property
    def first_name(self):
        return self.first_name_

    @first_name.setter
    def first_name(self, value):
        self.ex_log.error('Unable to rewrite FIRST_NAME')
        raise AttributeError("You can't change this field")

    @property
    def last_name(self):
        return self.last_name_

    @last_name.setter
    def last_name(self, value):
        self.ex_log.error('Unable to rewrite SECOND_NAME')
        raise AttributeError("You can't change this field")

    @property
    def birth_date(self):
        return self.birth_date_

    @birth_date.setter
    def birth_date(self, value):
        if not isinstance(value, str):
            raise_error(self.ex_log, 'type', 'birth_date', value)
        if re.match(r'\d{4}-\d{2}-\d{2}\b', value):
            self.log.info('{0} {1}: {2} was successfully set to {3}'.format(self.first_name,
                                                                            self.last_name, 'birth_date', value))
            self.birth_date_ = value
        else:
            raise_error(self.ex_log, 'value', 'birth_date', value)

    @property
    def phone(self):
        return self.phone_

    @phone.setter
    def phone(self, value):
        if not isinstance(value, str):
            raise_error(self.ex_log, 'type', 'phone', value)
        if re.search(r'[^\d()\-+ ]', value) is None:
            data = re.findall(r'\d+', value)
            data = ''.join(data)
            if len(data) == 11:
                self.log.info('{0} {1}: {2} was successfully set to {3}'.format(self.first_name,
                                                                                self.last_name, 'phone', value))
                self.phone_ = '8' + data[1:]
            else:
                raise_error(self.ex_log, 'value', 'phone', value)
        else:
            raise_error(self.ex_log, 'value', 'phone', value)

    @property
    def document_type(self):
        return self.document_type_

    @document_type.setter
    def document_type(self, value):
        if not isinstance(value, str):
            raise_error(self.ex_log, 'type', 'document_type', value)
        types = ('паспорт', 'заграничный паспорт', 'водительские права')
        if value in types:
            self.log.info('{0} {1}: {2} was successfully set to {3}'.format(self.first_name,
                                                                            self.last_name, 'document_type', value))
            self.document_type_ = value
        else:
            raise_error(self.ex_log, 'value', 'document_type', value)

    @property
    def document_id(self):
        return self.document_id_

    @document_id.setter
    def document_id(self, value):
        if not isinstance(value, str):
            raise_error(self.ex_log, 'type', 'document_id', value)
        if re.search(r'[^\d ]]', value) is None:
            value = re.findall(r'\d+', value)
            value = ''.join(value)
            if (len(value) == 10 and self.document_type_ != 'заграничный паспорт') or\
                    (len(value) == 9 and self.document_type_ == 'заграничный паспорт'):
                self.log.info('{0} {1}: {2} was successfully set to {3}'.format(self.first_name,
                                                                                self.last_name, 'document_id', value))
                self.document_id_ = value
            else:
                raise_error(self.ex_log, 'value', 'document_id', value)
        else:
            raise_error(self.ex_log, 'value', 'document_id', value)

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

