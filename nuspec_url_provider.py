import httpx


class NuspecUrlProvider:
    def __init__(self):
        self.__id = "https://api.nuget.org/v3-flatcontainer"


    def generate_nuspec(self, package: str, version: str) -> str:
        filename = "temp.nuspec"
        package = package.lower()

        res = httpx.get(f"{self.__id}/{package}/{version}/{package}.nuspec")
        res.raise_for_status()

        with open(filename, 'wb') as file:
            file.write(res.content)

        return filename