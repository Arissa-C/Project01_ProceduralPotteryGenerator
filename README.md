GitHub URL:
https://github.com/Arissa-C/Project01_ProceduralPotteryGenerator

Challenge Features:
- Places a group of pots according to user-defined parameters using spiral algorithm
- Randomizes pot heights and widths according to range given
- Paired sliders constrain each other; min never exceeds max and vice versa
- Slider labels display values
- All parameters grouped in neat sections
- Pot group name editable with input validation (uses custom validator class to only allow alphanumeric/underscore chars to be entered)
- Instead of running as normal, create button warns user if group name is invalid for maya (empty string or digit in first position)
- Reset button to return parameter values to defaults
- Colored pots

Current Limitations:
- Very simple pot mesh (low customizability for rims, roundedness of pots)
- When pots are short enough, the spherical top clips through bottom
- Mathematically formulaic, creates symmetric patterns, sometimes user doesn't want that
- Distribution algorithm is tight at center and sparse at edges due to how spirals work
- Tool doesn't prevent pots clipping into each other on certain settings
- Only one color option
