type SquareProps = {
  x: number;
  y: number;
  colour: string;
  image?: string;
};

function Square({ x, y, colour, image }: SquareProps) {
  return (
    <div
      className="square"
      style={{
        left: `${x}vw`,
        top: `${y}vh`,
        backgroundColor: colour,
      }}
    >
      {image && <img src={image} className="chess-piece" alt="Chess piece" />}
    </div>
  );
}

export default Square;