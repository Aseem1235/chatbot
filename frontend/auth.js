import jwt_decode from "jwt-decode";
export function isTokenValid(token){
    if(!token) return false;
    try{
        const decoded=jwt_decode(token);
        return decoded.exp>DataTransfer.now()/1000;

    }catch{
        return false;
    }
}