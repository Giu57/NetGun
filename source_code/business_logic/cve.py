import  requests, time
from pprint import pprint
    
class cve:
    results = {}
    path = "https://services.nvd.nist.gov/rest/json/cves/2.0?"
    versions: dict
    header ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                                "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    def __init__(self, versions: dict):
        assert versions is not None, "Version not exists"
        self.versions = versions

    def search_cve(self) :
        """ Research CVE given a group of services or a CPE from the Scan Result. 
        Return  a dictionary with Version, CVE-id, CVE description and resources where the user can read  """
        key_counter= 0
        results = {}
        if "cpe" in  self.versions:
            response_cpe = requests.get(self.path, params={"CPE": self.versions["CPE"] + "isVulnerable"}, headers=self.header)
            key_counter +=1
            results[key_counter] = cve.get_vulnerabilities(response_cpe.json(), self.versions["CPE"])
        for port, info in self.versions['ports'].items():
            if 'version' in info:
                response_version = requests.get(self.path, params = {"keywordSearch":  info["version"]}, headers=self.header)
                if response_version.status_code == 200:
                    data = response_version.json()
                    key_counter += 1
                    results[key_counter] = cve.get_vulnerabilities(data, info["version"])

        self.results = results
        return results

    @classmethod
    def get_vulnerabilities(cls, data: dict, version) -> dict:
        """ Create a dictionary with Version, CVE-id, CVE Description e References"""
        results = {"Version": version}
        for cve in data["vulnerabilities"]:
                results["id"] = cve["cve"]["id"]
                results["description"] = cve["cve"]["descriptions"]
                results["references"] = cve["cve"]["references"][:4]
        return results



"""versions = {
    'ports': {
        '21/tcp': {'service': 'ftp', 'version': 'vsftpd 2.3.4', 'state': 'open'},
        '22/tcp': {'service': 'ssh', 'version': 'OpenSSH 4.7p1 Debian 8ubuntu1', 'state': 'open'},
        '23/tcp': {'service': 'telnet', 'version': 'Linux telnetd ', 'state': 'open'},
        '25/tcp': {'service': 'smtp', 'version': 'Postfix smtpd ', 'state': 'open'},
        '53/tcp': {'service': 'domain', 'version': 'ISC BIND 9.4.2', 'state': 'open'},
        '80/tcp': {'service': 'http', 'version': 'Apache httpd 2.2.8', 'state': 'open'},
        '111/tcp': {'service': 'rpcbind', 'version': ' ', 'state': 'open'},
        '139/tcp': {'service': 'netbios-ssn', 'version': 'Samba smbd 3.X - 4.X', 'state': 'open'},
        '445/tcp': {'service': 'netbios-ssn', 'version': 'Samba smbd 3.X - 4.X', 'state': 'open'},
        '512/tcp': {'service': 'exec', 'version': ' ', 'state': 'open'},
        '513/tcp': {'service': 'login', 'version': 'OpenBSD or Solaris rlogind ', 'state': 'open'},
        '514/tcp': {'service': 'tcpwrapped', 'version': ' ', 'state': 'open'}
    },
    'status': 'up',
    'os': {'name': 'Linux 2.6.9 - 2.6.33', 'accuracy': '100'}
}
cve_element = cve(versions)
pprint(cve_element.search_cve())
"""