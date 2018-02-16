from functools import partial
import csv
from lxml import etree
from lxml.builder import E
import multiprocessing
import os
from random import choice
from random import randint
import string
import shutil
import tempfile
import time
import uuid
import zipfile


def timer(func):
    ''' Decorator to measure time consuming'''
    def wrapper(*args, **kwargs):
        ts = time.time()
        res = func(*args, **kwargs)
        msg = ("Time execution for function (%s) is - %s" %
               (func.__name__, time.time() - ts))
        print(msg)
        return res
    return wrapper


class Task(object):
    def __init__(self, f_num=100, z_num=50):
        self.z_num = z_num
        self.f_num = f_num

    def _get_str(self, root):
        ''' Transform Lxml object to string'''
        return etree.tostring(root, pretty_print=True, encoding='unicode')

    def _rand_str(self, num=20):
        '''
        Generate string with random symbols + numbers by specified length.
        The default length is 20 symbols.
        '''
        return ''.join(
            choice(string.ascii_letters + string.digits) for _ in range(num))

    def _rand_val(self, start=1, end=10):
        '''Generate random int value from specified interval'''
        return randint(start, end)

    def _get_content(self):
        '''Generate specific xml content'''
        root = (
            E.root(
                E.var(name='id', value=str(uuid.uuid4())),
                E.var(name='level', value=str(self._rand_val(1, 100))),
                E.objects(
                    *(
                        E.object(name=self._rand_str())
                        for _ in range(self._rand_val())
                    )
                )
            )
        )
        return self._get_str(root)

    def _create_zip(self, dir_name, num):
        '''
           dir_name param: name of the directory where will be created archives
           num param: number of the current zip archive.

           Creates temporary directory with name dir_name.
           Creates xml files with names file-X.xml, where X is a number of the
           file.
           Compress all xml files in zip file with name archive-Y.zip, where
           Y is equal 'num' paramater.
        '''
        name = '/'.join((dir_name, 'archive-%s.zip' % num))
        tmp_dir = tempfile.mkdtemp(dir_name)
        with zipfile.ZipFile(name, 'w') as z_f:
            for i in range(self.f_num):
                name = '/'.join((tmp_dir, 'file-%s.xml' % i))
                with open(name, 'w') as f:
                    f.write(self._get_content())
                z_f.write(name)
        shutil.rmtree(tmp_dir)

    @timer
    def first_part(self):
        '''
        Use multiprocessing to parallel creation all necessary zip archives.
        '''
        arch_dir = 'archives'
        os.makedirs(arch_dir, exist_ok=True)
        func = partial(self._create_zip, arch_dir)
        with multiprocessing.Pool() as p:
            p.map(
                func,
                (n for n in range(self.z_num))
            )

    def _parse_files(self, archive):
        '''
        Parser of the *.xml files.
        archive param: name of the zip archive to unpack and parse nested files

        Parse whole file, because it is small enough and we can ignore using
        iterator for parsing.
        Split all parsed data on two lists for future storing them in separate
        csv files.
        '''
        with zipfile.ZipFile(archive, 'r') as z_f:
            first_data = []
            second_data = []
            for f_name in z_f.namelist():
                with z_f.open(f_name) as f:
                    root = etree.fromstring(f.read())
                    var1 = root.findall('var')[0]
                    var2 = root.findall('var')[1]
                    if var1.get('name') == 'id':
                        _id, level = var1.get('value'), var2.get('value')
                    else:
                        _id, level = var2.get('value'), var1.get('value')
                    first_data.append((_id, level))

                    for i in root.find('objects').findall('object'):
                        second_data.append((_id, i.get('name')))
        return first_data, second_data

    def _write_result(self, data):
        ''' Write all prepared data to csv files '''
        csvfile_1 = open('1.csv', 'w', newline='')
        csvfile_2 = open('2.csv', 'w', newline='')
        writer1 = csv.writer(csvfile_1)
        writer2 = csv.writer(csvfile_2)
        for pair in data:
            for row in pair[0]:
                writer1.writerow(row)
            for row in pair[1]:
                writer2.writerow(row)

        csvfile_1.close()
        csvfile_2.close()

    @timer
    def second_part(self):
        '''
        Use multirocessing to parse files from archives and storing
        all data in "res" value for writing in csv files at the end.
        '''
        # NOTE: looks like simple threading works slower, then multiprocessing
        # (1.4 vs 0.7). Also threading takes about 40 % of each core, when
        # multiprocessing allocate about 90 % of each core.
        with multiprocessing.Pool() as p:
            res = p.map(
                self._parse_files,
                ('archives/%s' % z_f for z_f in os.listdir('archives'))
            )

        self._write_result(res)
        # NOTE: comment following line if you would like to
        # leave "archives" directory for verification
        shutil.rmtree('archives')

#    # experiment with Queue (it does not give huge performance growth)
#    def _parse_files_q(self, args):
#        q, archive = args
#        with zipfile.ZipFile(archive, 'r') as z_f:
#            first_data = []
#            second_data = []
#            for f_name in z_f.namelist():
#                with z_f.open(f_name) as f:
#                    root = etree.fromstring(f.read())
#                    var1 = root.findall('var')[0]
#                    var2 = root.findall('var')[1]
#                    if var1.get('name') == 'id':
#                       _id, level = var1.get('value'), var2.get('value')
#                    else:
#                       _id, level = var2.get('value'), var1.get('value')
#                    first_data.append((_id, level))
#
#                    for i in root.find('objects').findall('object'):
#                        second_data.append((_id, i.get('name')))
#        q.put((first_data, second_data))
#
#    def _write_result_q(self, q):
#        csvfile_1 = open('1.csv', 'w', newline='')
#        csvfile_2 = open('2.csv', 'w', newline='')
#        writer1 = csv.writer(csvfile_1)
#        writer2 = csv.writer(csvfile_2)
#        while not q.empty():
#            pair = q.get()
#            for row in pair[0]:
#                writer1.writerow(row)
#            for row in pair[1]:
#                writer2.writerow(row)
#
#        csvfile_1.close()
#        csvfile_2.close()
#
#    @timer
#    def second_part_q(self):
#        '''
#        I tried to use Queue to put data and write it in parallel with
#        other processes, but it looks like it will not give huge performance
#        increase, so I just leave it here as example.
#        '''
#        manager = multiprocessing.Manager()
#        q = manager.Queue()
#        with multiprocessing.Pool() as p:
#            p.map(
#                self._parse_files,
#                ((q, 'archives/%s' % z_f) for z_f in os.listdir('archives'))
#            )
#
#            p.map(
#                self._write_result, [q]
#            )
#        # leave this directory here for verification
#        # shutil.rmtree('archives')


if __name__ == '__main__':
    # Execute both parts of the task and print time consuming results for them
    t = Task()
    t.first_part()
    t.second_part()
