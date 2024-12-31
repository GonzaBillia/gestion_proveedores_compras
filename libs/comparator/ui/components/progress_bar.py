from PyQt5.QtWidgets import QProgressBar

class ProgressBar():
    @staticmethod
    def new(layout, min, max, value):
        progress_bar = QProgressBar()
        progress_bar.setMinimum(min)
        progress_bar.setMaximum(max)
        progress_bar.setValue(value)
        layout.addWidget(progress_bar)
        return progress_bar

    def update_progress(bar, value):
        if bar:
            bar.setValue(value)