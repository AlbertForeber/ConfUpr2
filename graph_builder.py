from typing import Dict
from graph_node import GraphNode
from nuspec_url_provider import NuspecUrlProvider
import xml.etree.ElementTree as ET


class GraphBuilder:
    def __init__(self, config: Dict):
        self.__test = config["data_mode"] == "test"
        self.__graph = {}
        self.__config = config


    def build_one_layer_graph_from_nuspec(self):
        provider = NuspecUrlProvider()

        url = self.__config['path'].split()[-1].lower()
        filename = provider.generate_nuspec(url, self.__config['version'])

        try:
            tree = ET.parse(filename)
        except ET.ParseError:
            raise ET.ParseError()

        tree.getroot().find()




    def build_graph(self, one_layer: bool = False) -> GraphNode:
        if one_layer:
            graph = self.build_one_layer_graph_from_nuspec()
        else:
            graph = self.__build_graph_from_nuspec() if self.__test else self.__build_graph_from_test()
        return graph


    def __build_graph_from_nuspec(self) -> GraphNode:
        pass


    def __build_graph_from_test(self) -> GraphNode:
        pass