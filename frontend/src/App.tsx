import whiteKing from "./assets/wK.svg";
import ChessBoard from "./components/ChessBoard";


function App() {
    return (
        <div className="app-layout">
            <ChessBoard
                chessColourWhite="rgb(199, 192, 131)"
                chessColourBlack="rgb(11, 63, 1)"
            />

            <div className="move-history">
                {/* Move history */}
            </div>

            <div className="side-panel">
                {/* Controls */}
            </div>
        </div>
    );
}


export default App;
