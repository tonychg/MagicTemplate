" Write Template with relative edit file path

let g:templatesDirectory = $HOME."/Templates/"

" All substitue are here
fun! WriteTemplate( templateFilePath )
    execute "0r ".a:templateFilePath
    execute "%s/$filename/".expand('%:t')."/ge"
    execute "%s/$timestamp/".strftime('%m\/%d\/%y')."  /ge"
    execute "%s/$year/".strftime('%Y')."/ge"
    execute "%s/$user/".$USER."/ge"
endfunction

fun! s:autoWriteTemplate ()
    let lineNbrs = line('$')
    let templateFilePath = ""

    if strlen(expand('%:t'))
        let templateName = expand('%:t')
        if templateName[0] == '.'
            let templateName = strpart(templateName, 1, len(templateName)-1)
        endif
        if filereadable(g:templatesDirectory.templateName)
            let templateFilePath = g:templatesDirectory.templateName
        endif
    endif

    if strlen(&filetype) && !strlen(templateFilePath)
        let templateFilePath = g:templatesDirectory.&filetype
        if &filetype == "html"
            let ext = expand('%:e')
            if ext == 'vue' && filereadable(g:templatesDirectory.ext)
                let templateFilePath = g:templatesDirectory.ext
            endif
        endif
    endif

    if lineNbrs == 1 && filereadable(templateFilePath)
        let choice = confirm("Auto write template ?", "&Yes\n&No", 1)
        if choice != 2
            call WriteTemplate ( templateFilePath )
        endif
    endif
endfunction

" Templates Write on New File
" autocmd BufNewFile * call s:autoWriteTemplate()
nnoremap <silent> <leader>t :call PythonWriteTemplate()<CR>
