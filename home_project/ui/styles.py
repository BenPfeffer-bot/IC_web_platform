class Styles:
    @staticmethod
    def get_animation_css() -> str:
        return """
        <style>
            .animation-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                width: 100vw;
                position: fixed;
                top: 0;
                left: 0;
                background-color: #f0f2f6;
                z-index: 9999;
            }

            header {visibility: hidden;}
            

            .logo-container {
                position: relative;
                width: 400px;
                height: 400px;
            }

            .rotating-circle {
                position: absolute;
                width: 100%;
                height: 100%;
                border: 4px solid rgba(115, 120, 127);
                border-radius: 50%;
                animation: rotate 10s linear infinite;
            }

            .rotating-circle::before {
                content: '';
                position: absolute;
                width: 20px;
                height: 20px;
                background: #161E29;
                border-radius: 50%;
                top: -10px;
                left: 50%;
                transform: translateX(-50%);
            }

            .gear-marks {
                position: absolute;
                width: 100%;
                height: 100%;
            }

            .gear-mark {
                position: absolute;
                width: 4px;
                height: 15px;
                background: #161E29;
                left: 50%;
                transform-origin: bottom center;
                opacity: 0;
                animation: fadeIn 0.5s forwards;
            }

            .inner-circle {
                position: absolute;
                width: 80%;
                height: 80%;
                border: 3px solid rgba(115, 120, 127);
                border-radius: 50%;
                top: 10%;
                left: 10%;
                animation: counterRotate 8s linear infinite;
            }

            .lines {
                position: absolute;
                width: 100%;
                height: 100%;
            }

            .horizontal-line, .vertical-line {
                position: absolute;
                background-color: #161E29;
            }

            .horizontal-line {
                width: 0;
                height: 4px;
                top: 50%;
                left: 0;
                animation: horizontalGrow 1.5s ease-in-out forwards;
            }

            .vertical-line {
                width: 4px;
                height: 0;
                left: 50%;
                top: 0;
                animation: verticalGrow 1.5s ease-in-out forwards;
            }

            .shapes {
                position: absolute;
                width: 100%;
                height: 100%;
                animation: rotate 8s linear infinite;
            }

            .shape {
                position: absolute;
                width: 80px;
                height: 80px;
                border: 4px solid #161E29;
                opacity: 0;
            }

            .shape1 {
                top: 20%;
                left: 20%;
                animation: fadeIn 1s ease-in-out forwards 0.5s;
            }

            .shape2 {
                bottom: 20%;
                right: 20%;
                animation: fadeIn 1s ease-in-out forwards 1s;
            }

            .logo {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                opacity: 0;
                animation: fadeIn 1s ease-in-out forwards 1.5s;
                z-index: 3;
            }

            .logo img {
                width: 200px;
                height: auto;
            }

            .gear {
                position: absolute;
                width: 500px;
                height: 500px;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                animation: rotateGear 20s linear infinite;
                pointer-events: none;
                z-index: 1;
            }

            .gear-tooth {
                position: absolute;
                width: 30px;
                height: 30px;
                background: rgba(22, 30, 41, 0.1);
                border: 3px solid #161E29;
                transform-origin: center;
                border-radius: 3px;
            }

            .logo-container > * {
                position: absolute;
                z-index: 2;
            }

            @keyframes horizontalGrow {
                0% { width: 0; }
                100% { width: 100%; }
            }

            @keyframes verticalGrow {
                0% { height: 0; }
                100% { height: 100%; }
            }

            @keyframes rotate {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            @keyframes counterRotate {
                0% { transform: rotate(360deg); }
                100% { transform: rotate(0deg); }
            }

            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }

            @keyframes rotateGear {
                from { transform: translate(-50%, -50%) rotate(0deg); }
                to { transform: translate(-50%, -50%) rotate(360deg); }
            }
        </style>
        <script>
            function createGearMarks() {
                const gearMarks = document.querySelector('.gear-marks');
                const numMarks = 60;
                
                for (let i = 0; i < numMarks; i++) {
                    const mark = document.createElement('div');
                    mark.className = 'gear-mark';
                    mark.style.transform = `rotate(${i * (360 / numMarks)}deg) translateX(-50%)`;
                    mark.style.animationDelay = `${i * (1 / numMarks)}s`;
                    gearMarks.appendChild(mark);
                }
            }

            function createGear() {
                const gear = document.querySelector('.gear');
                const numTeeth = 16;
                
                for (let i = 0; i < numTeeth; i++) {
                    const tooth = document.createElement('div');
                    tooth.className = 'gear-tooth';
                    const angle = (i * 360) / numTeeth;
                    const radius = 230;
                    
                    tooth.style.left = `calc(50% - 15px)`;
                    tooth.style.top = `calc(50% - 15px)`;
                    tooth.style.transform = `
                        rotate(${angle}deg) 
                        translate(${radius}px) 
                        rotate(${45}deg)
                    `;
                    
                    gear.appendChild(tooth);
                }
            }
            
            document.addEventListener('DOMContentLoaded', () => {
                createGearMarks();
                createGear();
            });
        </script>
        """

    @staticmethod
    def get_animation_html(logo_path: str) -> str:
        return f"""
        <div class="animation-container">
            <div class="logo-container">
                <div class="gear"></div>
                <div class="rotating-circle"></div>
                <div class="gear-marks"></div>
                <div class="inner-circle">
                <div class="lines">
                    <div class="horizontal-line">
                    <div class="vertical-line"></div>
                <div class="shapes">
                    <div class="shape shape1">
                    <div class="shape shape2"></div>
                </div>
                <div class="logo"> 
                    <img src="{logo_path}" alt="Logo"> 
                </div>
            </div>
        </div>
        """
