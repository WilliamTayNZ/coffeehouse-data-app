import "../pages-styles/Home.css";
import { useState } from "react";

import LogoHeader from '../components/LogoHeader';
import SubmitFile from '../components/SubmitFile';


const Home = () => {
    return (
    <div className="app-container">
        {<LogoHeader />}
        <hr className="divider" />
        <div className="bottom-section">
            {<SubmitFile />}
        </div>
    </div>
    );
};

export default Home;
