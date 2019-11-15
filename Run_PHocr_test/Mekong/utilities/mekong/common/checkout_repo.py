from git_checkout import GitCheckout
from svn_checkout import SVNCheckout
import os
from utilities import load_json

class CheckoutSCMMain:
    """Checking out repository for PHOcr project"""

    project = ''
    def __init__(self, project):
        self.project = project

    def checkout_repo(self, pj_config, tool_json, outdir, refspecs=None):
        scm_type = pj_config['type']
        repo_url = pj_config['repo']
        tool_location = tool_json[scm_type]
        credentical_name = pj_config['credentical']

        current_folder = os.path.dirname(os.path.abspath(__file__))
        credentical_path = os.path.join(current_folder, '..', 'config', 'credentical.json')
        err, credentical_json = load_json(credentical_path)

        auth = credentical_json[credentical_name]

        scm_getter = None
        if scm_type == 'git':
            scm_getter = GitCheckout(tool_location, repo_url, outdir, credentical=auth)
        elif scm_type == 'svn':
            scm_getter = SVNCheckout(tool_location, repo_url, outdir, credentical=auth)

        if scm_getter == None:
            message = 'SCM type "%s" not exist' % (scm_type)
            return [Exception(message), None]

        [err, is_ok] = scm_getter.checkout(refspecs)
        if err:
            return [err, None]

        return [None, is_ok]

    def run(self, tool, scm_json, out, refspecs):
        # Checking json data
        if not scm_json.has_key(self.project):
            message = 'Project "%s" is not configured in SCM config file' \
                      % (self.project)
            return [Exception(message), None]

        pj_config = scm_json[self.project]

        if not pj_config.has_key('type'):
            message = 'Project "%s" not have "type" field of SCM in config file' \
                      % (self.project)
            return [Exception(message), None]
        if not pj_config.has_key('repo'):
            message = 'Project "%s" not have "repo" field of SCM in config file' \
                      % (self.project)
            return [Exception(message), None]

        # Checkout main repo
        outdir = os.path.join(*out.split('/'))
        [err, result] = self.checkout_repo(pj_config, tool, outdir, refspecs)
        if err:
            return [err, None]

        # If not have key 3rd_parties --> return
        if not scm_json[self.project].has_key('3rd_parties'):
            return [None, True]

        parties = scm_json[self.project]['3rd_parties']
        for party_key in parties:
            if not scm_json.has_key(party_key):
                message = 'Third party %s of project "%s" not exist in config file' \
                          % (party_key, self.project)
                return [Exception(message), None]

        # Checkout 3rd_party
        for party_key in parties:
            party_outdir = os.path.join(outdir, *parties[party_key]['outdir'].split('/'))
            print(party_outdir)

            party_proj_config = scm_json[party_key]
            [err, result] = self.checkout_repo(party_proj_config, tool, party_outdir)
            if err:
                return [err, None]
