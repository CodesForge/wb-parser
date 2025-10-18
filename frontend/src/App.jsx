import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { useForm } from 'react-hook-form';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useLocation } from 'react-router-dom';
import './App.css'

function Profile() {
  const navigate = useNavigate();
  const [clicked, setClicked] = useState(false);
  const location = useLocation();

  const productData = location.state?.productData;

  const clickedButtonReturn = () => {
    navigate('/')
  }
  const WBOpenClickButton = () => {
    window.open(productData?.product_data?.product_url, '_blank');
  }

  return (
    <div className='flex justify-center items-center min-h-screen flex-col'>
      <div className='flex justify-center items-center flex-col border-[3px] h-130 rounded-[15px] border-[#58585833] bg-neutral-800 hover:scale-110 transition-all duration-300 ease-in-out hover:bg-[#2b2b2b] hover:border-[#64646433]'>
        <img className='w-35 -mt-11' src="src\assets\AnimatedStickerLupa-ezgif.com-gif-maker.gif" alt="magnifier" />
        <h1 className='font-semibold text-white text-[30px]'>Результаты поиска</h1>
      {productData?.product_data ? (
        <div className='bg-[#58585833] rounded-[10px] h-40 w-95 flex justify-center items-center flex-col mt-4'>
          <p className='text-white font-semibold text-center'>{productData.product_data.product_name}</p>
          <p className='text-white font-semibold'>Бренд: {productData.product_data.product_brand}</p>
          <p className='text-white font-semibold'>Цена: {productData.product_data.product_price} ₽</p>
          <p className='line-through text-gray-400 font-semibold'>Старая цена: {productData.product_data.product_price_basic} ₽</p>
          <p className='text-white font-semibold'>Рейтинг: ⭐{productData.product_data.product_rating}/5</p>
        </div>
      ) : (
        <p className='text-white font-semibold'>Данные не получены!</p>
      ) }
      <button onClick={clickedButtonReturn} className='bg-[#8774E1] hover:bg-[#6B5BB5] rounded-[10px] h-10 mt-6 w-50 text-white font-semibold transition-all duration-300 hover:shadow-lg hover:scale-105'>Новый поиск</button>
      <button onClick={WBOpenClickButton} className='bg-[#8774E1] hover:bg-[#6B5BB5] rounded-[10px] h-10 mt-6 w-50 text-white font-semibold transition-all duration-300 hover:shadow-lg hover:scale-105'>Открыть на WB</button>
      </div>
    </div>
  )
}

function MainClickButton() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [products, setProducts] = useState('');
  const {register, handleSubmit, formState} = useForm(
    {
      mode: "onChange",
    }
  )

  const OnSubmitClicker = async (data) => {
    console.log(data);
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/parsing-data', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(
          {
            "request_user": data["request_user"],
          }
        )
      })

      const dates = await response.json();
      setProducts(dates);
      console.log('Ответ от сервера:', dates);
      navigate("/parsing", {state: { productData: dates }});

    } catch (error) {
      console.log('Error:', error);
    } finally {
      setLoading(false);
    }
  }

  return(
    <div className='flex justify-center items-center min-h-screen flex-col'>
      <div className='mb-5'>
        <h1 className='text-[#ffffff] font-semibold flex justify-center text-[25px]'>Парсер Wildberries</h1>
        <h1 className='text-[#cccccc] font-semibold flex justify-center'>Введите название товара</h1>
      </div>
      <form className='flex flex-col' onSubmit={handleSubmit(OnSubmitClicker)}>
        <input className="hover:border-[#8774E1] placeholder:text-white focus:border-[2px] focus:border-[#8774E1] text-center bg-[#212121;] rounded-[10px] outline-0 font-semibold border-[#a0a0a0] border-[1px] h-10 w-70 text-white" placeholder='название товара' {...register("request_user", {required: "Invalid Syntax"})} ></input>
        <button className='bg-[#8774E1] hover:bg-[#6B5BB5] rounded-[10px] h-10 mt-4 text-white font-semibold transition-all duration-300 hover:shadow-lg hover:scale-105'>
        продолжить
      </button>
      </form>
    </div>
  )
}


function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<MainClickButton/>}/>
        <Route path='/parsing' element={<Profile/>}/>
      </Routes>
    </Router>
  )
}

export default App