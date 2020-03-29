from PipHome.PipLog import Logger


class PipConfig:
    _logger = Logger("PipConfig")

    def __init__(self, args):
        self._config = self._load_static_config()

    def config(self):
        return self._config.copy()

    def __getitem__(self, item):
        config = self._config
        for sub_item in item.split("."):
            config = config[sub_item]
        return config

    def _load_static_config(self):
        self._logger.info("Using static config")
        return {
            "gui": {
                "headless": False,
                "size": {
                    "width": 480,
                    "height": 320
                },
                "background": "#0D0208",
                "label": {
                    "foreground": "#008F11",
                    "background": "#0D0208"
                },
                "frame": {
                    "background": "#0D0208"
                },
                "button": {
                    "activebackground": "#008F11",
                    "activeforeground": "#0D0208",
                    "background": "#0D0208",
                    "foreground": "#008F11",
                    "font": "RobotoMono 16",
                    "borderwidth": 0
                },
                "listbox": {
                    "foreground": "#008F11",
                    "background": "#0D0208",
                    "font": "RobotoMono 16",
                    "highlightbackground": "#008F11",
                    "selectbackground": "#008F11",
                    "highlightcolor": "#008F11",
                    "selectforeground": "#0D0208",
                    "activestyle": "none",
                    "width": 10
                },
                "selected_tab": {
                    "foreground": "#0D0208",
                    "background": "#008F11"
                },
                "time_tab": {
                    # https://stackabuse.com/how-to-format-dates-in-python/
                    "date_format": "%a, %d %b %Y"
                }
            },
            "system": {
                "disk_check_path": "c:/"
            }
        }
