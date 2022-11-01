# NOTE: Do not symbolic link this script

readlink -e ~/.zshrc &> /dev/null
if [ $? != 0 ]; then
    echo -e '\e[31mError: $HOME/.zshrc does not exist.\n\tPlease check that the symbolic link is properly created and working.\e[m'
fi

readlink -e ~/.vimrc &> /dev/null
if [ $? != 0 ]; then
    echo -e '\e[31mError: $HOME/.vimrc does not exist.\n\tPlease check that the symbolic link is properly created and working.\e[m'
fi
