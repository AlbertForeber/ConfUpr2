from typing import Dict, List

from extras import DEBUG, EXTRA
from graph_node import GraphNode
from nuspec_url_provider import NuspecUrlProvider
import xml.etree.ElementTree as ET


class GraphBuilder:
    def __init__(self, config: Dict):
        self.__test = config["data_mode"] == "test"
        self.__graph = {}
        self.__config = config


    # TODO удалить после второго этапа
    def print_one_layer_graph(self):
        graph = self.__build_one_layer_graph_from_nuspec()
        print()
        print("-" * 40)
        print(DEBUG.format(graph.name))
        print("Dependencies:")
        for i in graph.dependencies:
            print(f"+ {EXTRA.format(i.name)}")


    def __build_one_layer_graph_from_nuspec(self):
        provider = NuspecUrlProvider()

        package_id = self.__config['path'].split('/')[-1]
        filename = provider.generate_nuspec(package_id.lower(), self.__config['version'])

        try:
            tree = ET.parse(filename)
        except ET.ParseError:
            raise ET.ParseError()

        root = tree.getroot()
        ns = {'ns': root.tag.split("}")[0][1:]}

        deps: List[ET.Element] = []

        for i in (tree.getroot()
                .find("ns:metadata", ns)
                .find("ns:dependencies", ns)
                .findall("ns:group", ns)):
            deps += i.findall("*")

        graph_node = GraphNode(package_id, self.__config["version"])

        for dep in deps:
            new_node = GraphNode(
                    dep.get("id", "unknown_id"),
                    dep.get("version", "_unknown_version_")[1:-1].split(',')[0]
                )

            if new_node not in graph_node.dependencies:
                graph_node.dependencies.append(new_node)
        return graph_node



    def build_graph(self, one_layer: bool = False) -> GraphNode:
        if one_layer:
            graph = self.__build_one_layer_graph_from_nuspec()
        else:
            graph = self.__build_graph_from_nuspec() if self.__test else self.__build_graph_from_test()
        return graph


    def __build_graph_from_nuspec(self) -> GraphNode:
        pass


    def __build_graph_from_test(self) -> GraphNode:
        pass