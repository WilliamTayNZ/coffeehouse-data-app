import MainLayout from '../components/MainLayout';
import ContentBox from '../components/ContentBox';
import { useNavigate } from 'react-router-dom';

const Home = () => {
    const navigate = useNavigate();

    return (
        <MainLayout>
            <ContentBox>
                <h1>Welcome to Sales Data Analyser!</h1>
                <button className="view-button" onClick={() => navigate('/clean-new-file')}>
                Clean new file
                </button>
                <button
                    className="view-button" onClick={() => navigate('/cleaned-sheets')}>
                    View cleaned sheets
                </button>
            </ContentBox>
        </MainLayout>
    );
};

export default Home;