from unittest import TestCase

from presenter.presenter import TextPresenter
from tasks import SimpleTasks


class TestPresenter(TestCase):
    def test_text_presenter_presents_tasks_correctly(self):
        tasks = SimpleTasks('work')
        tasks.add('tasks 1')
        tasks.add('tasks 2')
        tasks.add('tasks 3')
        tasks.add('tasks 4')
        tasks['tasks 1'].finish()
        tasks['tasks 4'].finish()
        expected = '    Work\n' \
                   '===========\n' \
                   '[x] tasks 1\n' \
                   '[ ] tasks 2\n' \
                   '[ ] tasks 3\n' \
                   '[x] tasks 4\n' \
                   '==========='
        self.assertEqual(expected, TextPresenter(tasks, 60).present())

    def test_text_presenter_presents_tasks_correctly_wraps_big_task_name(self):
        tasks = SimpleTasks('work')
        tasks.add('this is a long text!')
        expected = '    Work\n' \
                   '==================\n' \
                   '[ ] this is a long\n' \
                   '    text!\n' \
                   '=================='
        self.assertEqual(expected, TextPresenter(tasks, 18).present())

    def test_text_presenter_presents_tasks_correctly_wraps_mid_word(self):
        tasks = SimpleTasks('work')
        tasks.add('this is a long text!')
        expected = '    Work\n' \
                   '=================\n' \
                   '[ ] this is a lon\n' \
                   '    g text!\n' \
                   '================='
        self.assertEqual(expected, TextPresenter(tasks, 17).present())

    def test_text_presenter_presents_tasks_correctly_wraps_for_more_than_2_lines(self):
        tasks = SimpleTasks('work')
        tasks.add('this is a long text that needs wrapping!')
        expected = '    Work\n' \
                   '===================\n' \
                   '[ ] this is a long\n' \
                   '    text that needs\n' \
                   '    wrapping!\n' \
                   '==================='
        self.assertEqual(expected, TextPresenter(tasks, 19).present())
