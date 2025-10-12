from http.client import HTTPException
from typing import Dict, List, Tuple
from errors import *
from extras import DEBUG, EXTRA
from nuspec_url_provider import NuspecUrlProvider
import xml.etree.ElementTree as ET


def parse_dependencies_from_nuspec(root: ET.Element):
    ns = {'ns': root.tag.split("}")[0][1:]}

    deps: List[ET.Element] = []
    visited = set()

    try:
        if not root.find("ns:metadata", ns).find("ns:dependencies", ns):
            return deps

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
    except ET.ParseError:
        raise GBParseError


def from_xml_element_to_tuple(element: ET.Element) -> Tuple:
    return (
        element.get("id", "unknown_id"),
        element.get("version", "_unknown_version_").strip('[').strip(')').split(',')[0]
    )

class GraphBuilder:
    def __init__(self, config: Dict):
        self.__test = config["data_mode"] == "test"
        self.__path= config['path']
        self.__package_id = config["name"]
        self.__version = config['version']
        self.__filter = config['filter']

        self.__graph: Dict[Tuple, List[Tuple]] = {}


    def __build_one_layer_graph_from_nuspec(self) -> Dict:
        provider = NuspecUrlProvider(self.__path)

        try:
            root = provider.generate_nuspec(self.__package_id.lower(), self.__version)
        except:
            raise GBNuspecError

        deps = parse_dependencies_from_nuspec(root)

        self.__graph[(self.__package_id, self.__version)] = list()
        head = self.__graph[(self.__package_id, self.__version)]


        for dep in deps:
            head.append(
                from_xml_element_to_tuple(dep)
            )

        return self.__graph



    def build_graph(self, one_layer: bool = False) -> Dict:

        self.__graph = dict()

        if one_layer:
            self.__build_one_layer_graph_from_nuspec()
        else:
            self.__build_graph_from_nuspec() if not self.__test else self.__build_graph_from_test()
        return self.__graph


    def __build_graph_from_nuspec(self):
        provider = NuspecUrlProvider()

        visited = set()
        bfs = [(self.__package_id, self.__version)]

        for package in bfs:

            print(EXTRA.format(package[0]))

            try:
                root = provider.generate_nuspec(*package)
            except:
                raise GBNuspecError

            visited.add(package)

            deps = parse_dependencies_from_nuspec(root)


            self.__graph[package] = []

            for dep in deps:
                dep_tuple = from_xml_element_to_tuple(dep)
                if (dep_tuple not in visited) and (self.__filter not in dep_tuple[0]):
                    bfs.append(dep_tuple)
                    self.__graph[package].append(dep_tuple)


    def __build_graph_from_test(self):
        try:
            f = open(self.__path)
        except FileNotFoundError:
            raise GBFileNotFound

        for line in f:
            split_line = line.strip().split(':')
            package_name, deps = split_line[0], split_line[1].split(',')
            self.__graph[(package_name, "1.0.0")] = [(x.strip(), "1.0.0") for x in deps]

            print(f"{DEBUG.format(package_name)}:", ",".join(deps))


    def get_dependent_of(self, package_name: str, package_version: str) -> List:
        return [x for x in self.__graph if (package_name, package_version) in self.__graph[x]]

