import whiteKing from "./assets/wK.svg";
import ChessBoard from "./components/ChessBoard";

function App() {
  return (
    <ChessBoard
      x={10}
      y={10}
      size={80}
      chessColourWhite="rgb(199, 192, 131)"
      chessColourBlack="rgb(11, 63, 1)"
    />
  );
}

export default App;
