# Magic Template
Insert template file on new BuffEnter or Edit

Author:  TonyChG
License: MIT
URL: https://github.com/tonychg/

[![asciicast](https://asciinema.org/a/ZXySrXX4FYhQ556Xuz7G2KgMG.png)](https://asciinema.org/a/ZXySrXX4FYhQ556Xuz7G2KgMG)

# Usage
Default templates directory you can change it with:

```vim
let g:templatesDirectory = $HOME."/Templates/"
```

Template rely on the filename/filetype of the current buffer.

    For filename related:

    Create a LICENSE file in the templates directory
    When you open a new LICENSE file, MagicTemplate write the file LICENSE in
    the current buffer.

    For filetype related:

    Create a javascript file
    Template are write when vim enter a new javascript file


Template Variables

    You can configure substitution of template varaiables in MagicTempalte.vim
    In the function WriteTemlate() execute your substitute command.

