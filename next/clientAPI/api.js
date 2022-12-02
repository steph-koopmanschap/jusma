import axios from "axios";

// Client API functions that communicate with the API server

// Axios config
// const api = axios.create({
//     baseURL: process.env.API_SERVER_URL
// });

// Axios config
const api = axios.create({
    baseURL: "http://localhost:5000"
});

/* Auth Functions */

export async function login(email, password) {
    const response = await api.post("/api/auth/login", {email: email, password: password});
    return response.data;
}

export async function register(username, email, password) {
    const response = await api.post("/api/auth/register", {username: username, email: email, password: password});
    return response.data;
}

export async function logout() {
    const response = await api.post("/api/auth/logout");
    return response.data;
}
