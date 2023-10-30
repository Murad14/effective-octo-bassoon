import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from "./pages/LoginPage";
import RegisterPage from './pages/RegisterPage';
import LogoutPage from './pages/LogoutPage';
import { ToastContainer } from 'react-toastify';

function App() {
  return (
    <div className="App">
      <ToastContainer></ToastContainer>
      <BrowserRouter>
        <Routes>
          <Route path='/home' element={<HomePage />}></Route>
          <Route path='/login' element={<LoginPage />}></Route>
          <Route path='/register' element={<RegisterPage />}></Route>
          <Route path='/logout' element={<LogoutPage />}> </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
