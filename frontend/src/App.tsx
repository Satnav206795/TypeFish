import whiteKing from "./assets/wK.svg";
import Square from "./components/Square";

function App() {
  return (
    <div className="board">
      <Square x={0} y={0} colour="beige" image={whiteKing} />
      <Square x={12.5} y={0} colour="blue" />
    </div>
  );
}

export default App;
