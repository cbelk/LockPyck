general functionality of PyckTool

    request pre-terminal from PyckMaster

    replace the non-terminal portion of the pre-terminal with entries in freak file
    associated with that particular non-terminal, Note: freak sheets
    are sorted in descending order of frequency => process one line at a time

    hash each string resulting from replacing the non-terminal in the pre-terminal
    with an entry in the freak file

    compare hashed string to original hashed password, if the hashes match, then
    the password is the string used to generate the hash

    return success to PyckMaster

    request next pre-terminal
