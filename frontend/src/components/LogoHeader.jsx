import logo from "../assets/logo.png";    
import "../components-styles/LogoHeader.css";

const LogoHeader = () => {
    return (
    <div className="logo-header">
        <img src={logo} className="logo" alt="HouseOfCoffeesLogo" />
        <h1>Sales Data Analyser</h1>
    </div>
    )
};

export default LogoHeader;