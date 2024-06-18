// problemViewer.js
import { useMemo } from "react";

interface TextProps {
  text: string;
  align: string;
  border: boolean;
  title: string;
  disablePink: boolean;
}

interface ImageProps {
  url: string;
  width: number;
}

interface Problem {
  type: string;
  text?: string;
  align?: string;
  border?: boolean;
  url?: string;
  math?: string;
  title?: string;
}

interface ProblemViewerProps {
  array: Problem[];
  width: number;
  disablePink: boolean;
}

const Text = ({ text, align, title, disablePink }: TextProps) => {
  const inSide = useMemo(() => {
    const token = text?.split(" ")?.filter((v) => {
      return v;
    });
    let isBoldOn = false;
    let isItalicOn = false;
    let isUnderlineOn = false;
    return token.map((v, i) => {
      if (v === "<b>") {
        isBoldOn = true;
        return null;
      } else if (v === "</b>") {
        isBoldOn = false;
        return null;
      } else if (v === "<i>") {
        isItalicOn = true;
        return null;
      } else if (v === "</i>") {
        isItalicOn = false;
        return null;
      } else if (v === "<u>") {
        isUnderlineOn = true;
        return null;
      } else if (v === "</u>") {
        isUnderlineOn = false;
        return null;
      } else if (v === "<nl/>") {
        return <div style={{ width: 600, height: 18 }}></div>;
      } else if (v === "<t/>") {
        return (
          <span
            style={{
              fontWeight: isBoldOn ? "bold" : "normal",
              fontStyle: isItalicOn ? "italic" : "normal",
              textDecoration: isUnderlineOn ? "underline" : "none",
              marginLeft: 4,
              marginBottom: 10,
            }}
          >
            ㅤㅤㅤㅤㅤㅤ
          </span>
        );
      } else {
        return (
          <span
            key={i}
            style={{
              fontWeight: isBoldOn ? "bold" : "normal",
              fontStyle: isItalicOn ? "italic" : "normal",
              textDecoration: isUnderlineOn ? "underline" : "none",
              marginLeft: 4,
              backgroundColor:
                v?.length === 1 && !disablePink ? "pink" : "transparent",
              marginBottom: 10,
            }}
          >
            {v}
          </span>
        );
      }
    });
  }, [disablePink, text]);
  return (
    <div
      style={{
        position: "relative",
        paddingTop: title ? 5 : 0,
        alignItems: "center",
        display: "flex",
      }}
    >
      {title && (
        <div
          style={{
            position: "absolute",
            top: 0,
            width: 600,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <span
            style={{
              backgroundColor: "white",
              display: "flex",
              width: "auto",
              height: 20,
              lineHeight: 1,
              verticalAlign: "sub",
            }}
          >
            {"<"}
            {title}
            {">"}
          </span>
        </div>
      )}
      <div
        style={{
          height: "auto",
          border: "1px solid black",
          flexWrap: "wrap",
          justifyContent: align,
          width: 600,
          overflow: "visible",
          lineHeight: 1,
          paddingTop: 20,
          paddingBottom: 20,
          display: "flex",
          flexDirection: "row",
          alignItems: "center"
        }}
      >
        {inSide}
      </div>
    </div>
  );
};
const Image = ({ url, width }: ImageProps) => {
  return (
    <img
      src={url.includes(".") ? url : `data:image/jpeg;base64,${url}`} // url if contains '.', else base64
      // https://img-cf.kurly.com/shop/data/goodsview/20201012/gv10000126356_1.jpg
      style={{
        width: width,
        height: "auto",
        objectFit: "contain",
      }}
    />
  );
};
const ProblemViewer = ({ array, width, disablePink }: ProblemViewerProps) => {
  return (
    <div
      style={{
        height: "auto",
        width: width,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center"
      }}>
      {array.map((v, idx) => {
        const { type, text, align, border, url, math, title } = v;
        if (type === "math") {
          return (
            <Text
              key={idx}
              text={math ? math : ""}
              border={border ? border : false}
              title={title ? title: ""}
              align={""}
              disablePink={false}
            />
          );
        } else if (type === "image") {
          return <Image key={"image" + idx} width={600} url={url ? url : ""} />;
        } else {
          return (
            <Text
              align={align ? align : ""}
              key={"text" + idx}
              border={border ? border : false}
              text={text || ""}
              title={title ? title : ""}
              disablePink={disablePink}
            />
          );
        }
      })}
    </div>
  );
};
export default ProblemViewer;