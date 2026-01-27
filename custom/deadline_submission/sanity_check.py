"""
Nuke Deadline Submitter by Gilles Vink (2022)

Module to perform sanity check on script and node.

Will check for basic things like is the script saved, is
it modified, or is the file path in the write node added.

License check is also added, so if there are any nodes
in the __init__ license_nodes dictionary added, it will
scan for them. If found, a license limit will be added to
the submission.

Other checks can be added via this module.

"""

import nuke


class SanityCheck(object):
    def __init__(self):
        """
        Via this function nodes can be added that have a limited amount
        of available license.

        Add the Class name to the key, and add the amount
        of licenses in the value.

        This functionality is not provided by default in Deadline, so
        it can provide a way to implement into your own farm.

        If you haven't integrated a license limiting function, you can ignore
        the license check.

        This script only functions as a sanity check.
        """

        # Dictionary with nodes dependant on a limited
        # amount of licenses (NeatVideo, OpticalFlares, Mocha, etc)

        self.license_nodes = {
            "OFXcom.absoft.neatvideo5_v5": 10,
        }

    def validate_script(self, node):
        """
        This function can be called for validating the script.

        It will return a dictionary containing
        validated and license limit keys.

        If the key 'validated' is False, the submission will be canceled.

        The output will be something like this:

        {
            "validated": True
            "limit_groups": 5
        }

        So the script will proceed with submission, but it will have
        a LicenseLimit key added to the submission.

        This is a functionality Deadline doesn't provide by default, but
        it can be built in the balancing of jobs.

        Custom validation checks can be added in this function.

        """

        # Create initial validation dictionary, if this is returned the
        # submission will be aborted.
        validated = {
            "validated": False,
            "limit_neat": 0,
        }

        # Validate script
        script_validated = self.__script_validation()
        if not script_validated:
            return validated

        # Validate provided node
        node_validated = self.__node_validation(node)
        if not node_validated:
            return validated

        # Check for license limiting nodes
        limit_neat = self.__limit_neat()

        # If there are license limiting nodes, but user
        # doesn't want to submit these, abort submission
        if limit_neat is True:
            return validated

        # If user still wants to submit, add
        # license limit to validation dictionary
        elif limit_neat > 0:
            validated["limit_neat"] = limit_neat

        # Script is validated, change key so submission will continue
        validated["validated"] = True

        return validated

    @staticmethod
    def __script_validation():
        """
        Function to validate Nuke script.

        It will check if the script is saved or
        if it has been modified.
        """

        # Check for script path
        script_path = nuke.root().name()

        # If name is 'Root', it is not saved
        if script_path == "Root":
            nuke.critical(
                "The script is not saved, please"
                "\n"
                "save the script before submitting."
            )
            return False

        # If script is modified, ask if it is okay to save the file
        if nuke.modified():
            save = nuke.ask(
                "The script is modified, would you like to save it?"
            )

            # If user agrees, save file
            if save:
                nuke.scriptSave()
            else:
                return False

        # Script is validated
        return True

    @staticmethod
    def __node_validation(node):
        """
        Function to validate provided node.

        Will check if the file knob has been set.

        Other node checks can be added here.
        """

        # If filepath is empty, node is not validated
        file_path = node.knob("file").value()
        if file_path == "":
            nuke.critical("No filepath has been set.")
            return False

        # Write node is validated
        return True

    def __limit_neat(self):
        """
        Function to check for license limiting nodes
        in the script.
        """

        # Get dictionary with license limiting nodes
        license_nodes = self.license_nodes

        # Set initial lists so we can add values
        limiting_nodes = []

        # Iterate through the provided nodes
        for license_node in license_nodes.keys():

            # Search for nodes with the provided classes
            nodes = nuke.allNodes(license_node)

            # If nodes found, proceed searching
            if nodes:

                # Iterate trough each node in this class
                for node in nodes:

                    if node.Class() == "OFXcom.absoft.neatvideo5_v5":

                        # Only proceed if node is not disabled
                        if not node.knob("disable").value():

                            limiting_nodes.append(node.name())

        # If no limiting nodes found, nothing to worry about
        if limiting_nodes:

            # Ask the user if user would like to proceed with a license limit
            proceed = nuke.ask(
                "There are nodes active in the script with limited licenses %s."
                "\nIf you submit the script will render with a license limit."
                "\n\n"
                "Would you like to proceed?" % (limiting_nodes,)
            )

            # If yes, return the limit
            if proceed:
                return len(limiting_nodes)

            # If no, return a license limit found so validation failed
            else:
                return True

        # If not found, nothing to worry about
        else:
            return False