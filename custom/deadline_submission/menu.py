import nuke
import deadline_submission

menubar = nuke.menu("Nuke")
deadline_menu = menubar.addMenu("&Render")

deadline_menu.addCommand("-", "", "")

deadline_menu.addCommand(
    "Submit to Deadline",
    "deadline_submission.DeadlineSubmission().submit_selected_node()",
    "F9",
)
