from typing import Dict, List, Tuple

from extras import DEBUG, EXTRA
from nuspec_url_provider import NuspecUrlProvider
import xml.etree.ElementTree as ET


def parse_dependencies(root: ET.Element):
    ns = {'ns': root.tag.split("}")[0][1:]}

    deps: List[ET.Element] = []
    visited = set()

    for i in (root
            .find("ns:metadata", ns)
            .find("ns:dependencies", ns)
            .findall("ns:group", ns)):

        for j in i.findall("*"):
            to_check = ' '.join([j.get("id"), j.get("version")])
            if to_check not in visited:
                visited.add(to_check)
                deps.append(j)

    return deps


class GraphBuilder:
    def __init__(self, config: Dict):
        self.__test = config["data_mode"] == "test"
        self.__package_id = config['path'].split('/')[-1]
        self.__version = config['version']
        self.__filter = config['filter']

        self.graph: Dict[Tuple, List[Tuple]] = {}

    # TODO удалить после второго этапа
    def print_one_layer_graph(self):
        graph = self.__build_one_layer_graph_from_nuspec()
        print()
        print("-" * 40)

        print("Dependencies:")
        for package in graph:
            print(DEBUG.format(package[0]))
            for dep in graph[package]:
                print(f"+ {EXTRA.format(dep[0])}")


    def __build_one_layer_graph_from_nuspec(self) -> Dict:
        provider = NuspecUrlProvider()

        root = provider.generate_nuspec(self.__package_id.lower(), self.__version)
        deps = parse_dependencies(root)

        self.graph[(self.__package_id, self.__version)] = list()
        head = self.graph[(self.__package_id, self.__version)]


        for dep in deps:
            head.append(
                (
                    dep.get("id", "unknown_id"),
                    dep.get("version", "_unknown_version_")[1:-1].split(',')[0]
                )
            )

        return self.graph



    def build_graph(self, one_layer: bool = False) -> Dict:
        if one_layer:
            graph = self.__build_one_layer_graph_from_nuspec()
        else:
            graph = self.__build_graph_from_nuspec() if self.__test else self.__build_graph_from_test()
        return graph


    def __build_graph_from_nuspec(self) -> Dict:
        provider = NuspecUrlProvider()

        package_id = self.__config['path'].split('/')[-1]
        root = provider.generate_nuspec(package_id.lower(), self.__version)

        ns = {'ns': root.tag.split("}")[0][1:]}

        visited = set()
        bfs = []







    def __build_graph_from_test(self) -> Dict:
        pass