import axios from 'axios'


export const getFiles = async (dir: string,origin:string) => {
    // console.log('getFiles', {dir:dir,origin:origin})
    const res = await axios.post(`api/file/listdir/`, {dir:dir,origin:origin})
    return res.data
}

export const initFiles = async () => {
    const res = await axios.get(`api/file/listdir/`)
    return res.data
}