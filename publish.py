#! /usr/bin/env python
# encoding: UTF-8

import jinja2
import datetime
import shutil
import os.path
import togetter

class Publisher(object):

    def __init__(self, togetters):
        self.togetters = togetters
        self.title = togetters[0].title
        self.export_dir = 'work/%s' % self.title

    def copy_to_work(self):
        shutil.copytree('templates', self.export_dir)

    def remove_work_dir(self):
        work_dir = 'work'
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)

    def publish(self):

        self.remove_work_dir()
        self.copy_to_work()

        publish_date = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates/OEBPS/', encoding='utf8'))


        def write(file_name, data, chap=None):
            tpl = env.get_template('%s.jinja2' % file_name)
            if chap is not None:
                file_name = ('%d.' % chap).join(file_name.split('.'))
            with open('%s/OEBPS/%s' % (self.export_dir, file_name), 'w') as f:
                f.write(tpl.render(data))

        write('content.opf', { 'title': self.title, 'publish_date': publish_date, 'togs': self.togetters })
        write('title_page.xhtml', { 'title': self.title, 'publish_date': publish_date })
        write('navdoc.html', { 'title': self.title, 'togs': self.togetters })
        write('toc.ncx', { 'title': self.title, 'togs': self.togetters })
        for i, tog in enumerate(self.togetters):
            write('chap.xhtml', {'tog': tog}, i + 1)



if __name__ == "__main__":
    tog1 = togetter.Togetter(1)
    tog1.title = 'タイトル1'
    tog1.entries = ['あいう', 'abc']
    tog2 = togetter.Togetter(2)
    tog2.title = 'タイトル2'
    tog2.entries = ['あいう', 'abc']

    pub = Publisher([tog1, tog2])
    pub.publish()

