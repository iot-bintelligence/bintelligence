import './Homepage.css'
import Header from '../components/Header/Header'
import Content from '../components/Main content/Content'
import Footer from '../components/Footer/Footer'



function Homepage() {
    return (
      <div className="container">
        <Header />
        <Content />
        <Footer />
      </div>
    );
  }
  
  export default Homepage;