#! /usr/bin/env python
# encoding: UTF-8

import jinja2
import datetime
import shutil
import os
import togetter
import zipfile
import glob

class Publisher(object):

    def __init__(self, togetters):
        self.togetters = togetters
        self.title = togetters[0].title
        self.folder_name = self.title.replace('/', '_').replace(' ', '_')
        self.export_dir = 'work/%s' % self.folder_name

    def copy_to_work(self):
        shutil.copytree('templates', self.export_dir)

    def remove_work_dir(self):
        work_dir = 'work'
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)

    def create_dist_dir(self):
        dist_dir = 'dist'
        if not os.path.exists(dist_dir):
            os.mkdir(dist_dir)

    def publish(self):

        self.remove_work_dir()
        self.copy_to_work()
        self.create_dist_dir()

        publish_date = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        env = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates/OEBPS/', encoding='utf8'), autoescape=True)

        def write(file_name, data, chap=None):
            tpl = env.get_template('%s.jinja2' % file_name)
            if chap is not None:
                file_name = ('%d.' % chap).join(file_name.split('.'))
            with open('%s/OEBPS/%s' % (self.export_dir, file_name), 'w') as f:
                f.write(tpl.render(data))

        write('content.opf', { 'title': self.title, 'tids': '.'.join(map(lambda tog: str(tog.tid), self.togetters)), 'publish_date': publish_date, 'togs': self.togetters })
        write('title_page.xhtml', { 'title': self.title, 'publish_date': publish_date, 'togs': self.togetters })
        write('navdoc.html', { 'title': self.title, 'togs': self.togetters })
        write('toc.ncx', { 'title': self.title, 'togs': self.togetters })
        for i, tog in enumerate(self.togetters):
            write('chap.xhtml', {'tog': tog}, i + 1)

        # remove template files in work directory
        for j2 in glob.glob('%s/OEBPS/*.jinja2' % self.export_dir):
            os.remove(j2)

        # zip
        os.chdir('work')
        with zipfile.ZipFile('../dist/%s.epub' % self.folder_name, 'w') as epub:
            epub.write('%s/mimetype' % self.folder_name, 'mimetype')
            epub.write('%s/META-INF/' % self.folder_name, 'META-INF/', zipfile.ZIP_DEFLATED)
            epub.write('%s/META-INF/container.xml' % self.folder_name, 'META-INF/container.xml', zipfile.ZIP_DEFLATED)
            epub.write('%s/OEBPS/' % self.folder_name, 'OEBPS/', zipfile.ZIP_DEFLATED)
            for content in os.listdir('%s/OEBPS/' % self.folder_name):
                epub.write('%s/OEBPS/%s' % (self.folder_name, content), 'OEBPS/%s' % content, zipfile.ZIP_DEFLATED)


if __name__ == "__main__":
    tog1 = togetter.Togetter(1)
    tog1.title = 'Lorem ipsum'
    tog1.entries = ['Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.']
    tog2 = togetter.Togetter(2)
    tog2.title = '枕草子'
    tog2.entries = ['春は曙（あけぼの）。やうやう白くなりゆく山際（やまぎわ）、すこしあかりて、紫だちたる雲の細くたなびきたる。',
            '夏は夜。月の頃はさらなり、闇もなほ、螢（ほたる）飛びちがひたる。雨など降るも、をかし。',
            '秋は夕暮（ゆうぐれ）。夕日のさして山端（やまぎわ）いと近くなりたるに、烏（からす）の寝所（ねどころ）へ行くとて、三つ四つ二つなど、飛び行くさへあはれなり。まして雁（かり）などのつらねたるが、いと小さく見ゆる、いとをかし。日入（ひい）りはてて、風の音（おと）、蟲の音（ね）など。（いとあはれなり。）',
            '冬はつとめて。雪の降りたるは、いふべきにもあらず。霜などのいと白きも、またさらでも いと寒きに、火など急ぎおこして、炭（すみ）持てわたるも、いとつきづきし。昼になりて、ぬるくゆるびもていけば、炭櫃（すびつ）・火桶（ひおけ）の火も、白き灰がちになりぬるは わろし。']

    pub = Publisher([tog1, tog2])
    pub.publish()

