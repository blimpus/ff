import PySimpleGUI as psg

layout = [[psg.Text("Fantasy football analysis")],
          [psg.Text("ROS for all positions rest of season outlook")],
          [psg.Text("Next week to show next week predictions and comparison between players")],
          [psg.Text("Trade values for positional trade value")],
          [psg.Button("ROS")],
          [psg.Button("Next Week")],
          [psg.Button("Trade Values")]]

position_layout = [[psg.Text("pick the position you want to report on")],
                   [psg.Button("all positions")],
                   [psg.Button("RB")],
                   [psg.Button("QB")],
                   [psg.Button("FLEX")],
                   [psg.Button("DST")],
                   [psg.Button("K")],
                   [psg.Button("WR")]]

comparison_layout = [[psg.Text("would you like to compare two players from the results?")],
                     [psg.Button("yes")],
                     [psg.Button("no")]]


window = psg.Window("ff", layout, margins=(250, 250))
position_window = psg.Window("ff", position_layout, margins=(250, 250))
compare_window = psg.Window("ff", comparison_layout, margins=(250, 250))


def create_player_combobox(players):
    comparison_player_dropbox_combo = psg.Combo(players, font=('Times New Roman', 12), expand_x=True,
                                                enable_events=True,
                                                readonly=False, key='-COMBO-')
    return [[comparison_player_dropbox_combo, psg.Button('exit')]]


def create_player_dropdown_window(players):
    real_player_compare_window = psg.Window('combobox example',
                                            create_player_combobox(players),
                                            size=(750, 200))
    return real_player_compare_window
