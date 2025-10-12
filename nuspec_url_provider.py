import httpx
import xml.etree.ElementTree as ET


class NuspecUrlProvider:
    def __init__(self, nuspec_api_id: str = "https://api.nuget.org/v3-flatcontainer"):
        self.__id = nuspec_api_id


    def generate_nuspec(self, package: str, version: str) -> ET.Element:
        filename = "temp.nuspec"
        package = package.lower()

        res = httpx.get(f"{self.__id}/{package}/{version}/{package}.nuspec")
        res.raise_for_status()

        with open(filename, 'wb') as file:
            file.write(res.content)

        try:
            tree = ET.parse(filename)
        except ET.ParseError:
            raise ET.ParseError()

        return tree.getroot()