import LogoHeader from './LogoHeader';
import '../components-styles/MainLayout.css';

const MainLayout = ({ children }) => (
  <div className="app-container">
    <LogoHeader />
    <hr className="divider" />
    <div className="bottom-section">
      {children}
    </div>
  </div>
);

export default MainLayout; 