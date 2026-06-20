import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-gradient-to-b from-soccer-green to-soccer-dark text-white">
      <h1 className="text-5xl font-bold mb-4">SoccerMind AI</h1>
      <p className="text-xl mb-8">Точные футбольные прогнозы на основе машинного обучения</p>
      <div className="flex space-x-4">
        <Link href="/predictions" className="px-6 py-3 bg-white text-soccer-green rounded-full font-semibold hover:bg-gray-100 transition">
          Смотреть прогнозы
        </Link>
        <Link href="/login" className="px-6 py-3 border border-white text-white rounded-full font-semibold hover:bg-white hover:text-soccer-green transition">
          Войти
        </Link>
      </div>
      <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="p-6 bg-white/10 rounded-2xl backdrop-blur">
          <h3 className="text-2xl font-bold">AI-модели</h3>
          <p>Используем XGBoost, LightGBM, CatBoost с Optuna-тюнингом.</p>
        </div>
        <div className="p-6 bg-white/10 rounded-2xl backdrop-blur">
          <h3 className="text-2xl font-bold">Данные</h3>
          <p>xG, коэффициенты, травмы, история — более 50 признаков.</p>
        </div>
        <div className="p-6 bg-white/10 rounded-2xl backdrop-blur">
          <h3 className="text-2xl font-bold">ROI +35%</h3>
          <p>Средний возврат инвестиций наших пользователей.</p>
        </div>
      </div>
    </div>
  );
}