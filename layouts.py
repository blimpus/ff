import PySimpleGUI as psg

layout = [[psg.Text("fantasy football analysis download. \n choose ROS for rest of season projections or\n Next Week for \
weekly projections and comparison")],[psg.Button("ROS")],[psg.Button("Next Week")]]

position_layout = [[psg.Text("pick the position you want to report on")],[psg.Button("all positions")],[psg.Button("RB")],[psg.Button("QB")], [psg.Button("FLEX")], [psg.Button("DST")],[psg.Button("K")],[psg.Button("WR")]]

comparison_layout = [[psg.Text("would you like to compare two players from the results?")], [psg.Button("yes")], [psg.Button("now")]]