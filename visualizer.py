from typing import Dict, Tuple, List
import os
from extras import EXTRA, DEBUG


class Visualizer:
    def __init__(self, graph: Dict[Tuple, List[Tuple]], show_ascii: bool = False):
        self.__graph = graph



    def create_picture(self):
        file = open("temp.d2", "w")

        for package in self.__graph:
            parent = f"{package[0]} ({package[1]})"
            for dep in self.__graph[package]:
                file.write(f'"{parent}" -> "{dep[0]} ({dep[1]})"\n')


        os.popen("d2 --layout=elk temp.d2 temp.png")


    def draw_ascii(self):
        for i in self.__graph:
            visited = set()
            self.__draw_ascii_recursively(i, 0, visited, True)
            print("-"*40)

    def __draw_ascii_recursively(self, current_package, spaces, visited, formatted = False):
        to_format = EXTRA if formatted else DEBUG
        print(spaces * ' ', '└──', to_format.format(f"{current_package[0]} ({current_package[1]})"))
        for j in self.__graph[current_package]:
            if j in self.__graph:
                if j not in visited:
                    visited.add(j)
                    self.__draw_ascii_recursively(j, spaces + 4, visited)
                else:
                    print((spaces + 4) * ' ', '└──', to_format.format(f"{j[0]} ({current_package[1]})"))
